"""
RAG (Retrieval-Augmented Generation) System
Combines vector retrieval with LLM generation for contextual responses.
"""

import logging
from typing import List, Dict, Any, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from .config import (
    EMBEDDING_MODEL_NAME,
    CHROMA_DB_DIR,
    CHROMA_COLLECTION_NAME
)
from .llm_service import call_llm, call_local_llm, call_openai_llm, call_gemini_llm
from .llm_utils import (
    classify_intent,
    get_chat_history_context,
    resolve_product_reference,
    format_rag_context,
    is_safe_query,
    get_specialized_prompt,
    get_agent_name,
    should_resolve_product_context,
    should_use_chat_history,
    format_sales_response
)
from .order_processor import order_processor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGSystem:
    """
    Complete RAG system with retrieval and generation capabilities.
    """
    
    def __init__(self, llm_provider: str = "local"):
        self.llm_provider = llm_provider
        self.retriever = None
        self._initialize_retriever()
    
    def _initialize_retriever(self):
        """Initialize the vector store retriever"""
        try:
            # Initialize embedding model
            embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
            
            # Load vector store
            vectorstore = Chroma(
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=embedding_model,
                persist_directory=CHROMA_DB_DIR
            )
            
            # Create retriever
            self.retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}  # Top 5 similar documents
            )
            
            logger.info("RAG retriever initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize retriever: {e}")
            raise
    
    def retrieve_relevant_documents(self, query: str, k: int = 5) -> List[str]:
        """
        Retrieve relevant documents from vector store.
        
        Args:
            query: User query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document contents with product IDs included
        """
        try:
            # Update retriever with new k value
            self.retriever.search_kwargs = {"k": k}
            
            # Retrieve documents
            documents = self.retriever.get_relevant_documents(query)
            
            # Extract content from documents and include product_id if available
            doc_contents = []
            for doc in documents:
                content = doc.page_content
                # Add product_id to content if available in metadata
                if hasattr(doc, 'metadata') and doc.metadata and 'product_id' in doc.metadata:
                    product_id = doc.metadata['product_id']
                    # Insert product_id after the first line (Product: ...)
                    lines = content.split('\n')
                    if lines:
                        lines.insert(1, f"Product ID: {product_id}")
                        content = '\n'.join(lines)
                doc_contents.append(content)
            
            logger.info(f"Retrieved {len(doc_contents)} relevant documents")
            return doc_contents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    

    def generate_response(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[str] = None,
        cart_service=None,
        product_service=None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using RAG with enhanced order processing capabilities.
        
        Args:
            query: User query
            chat_history: Previous conversation context
            session_id: User session ID for cart management
            cart_service: Cart service instance for order processing
            product_service: Product service instance
            user_id: User ID for cart operations (guest user for chat sessions)
            
        Returns:
            Dictionary containing response and metadata with order processing info
        """
        try:
            # Step 1: Classify intent (now includes order_taking, cart_management, etc.)
            intent = classify_intent(query)
            
            # Step 2: Handle cart management requests specifically
            if intent == "cart_management" and cart_service and session_id:
                cart_summary = order_processor.get_cart_summary(session_id, cart_service, user_id)
                
                if cart_summary.get("empty", True):
                    response_text = cart_summary.get("message", "Your cart is empty.")
                else:
                    response_text = cart_summary["formatted_summary"]
                    response_text += "\n\n🛒 **Cart Actions Available:**"
                    response_text += "\n- Say 'remove [item]' to delete items"
                    response_text += "\n- Say 'checkout' or 'place order' to proceed"
                    response_text += "\n- Say 'add more' to continue shopping"
                
                return {
                    "response": str(response_text) if response_text is not None else "",
                    "intent": str(intent) if intent is not None else "cart_management",
                    "agent": str(get_agent_name(intent)) if get_agent_name(intent) is not None else "Cart Management Specialist",
                    "sources": [],
                    "context": "",
                    "products": [],
                    "metadata": {"cart_action": True, "cart_data": cart_summary},
                    "chat_history_used": False,
                    "product_context_used": False,
                    "order_processing": {
                        "has_cart_action": True,
                        "cart_summary": cart_summary
                    }
                }
            
            # Step 2b: Handle checkout requests
            if intent == "checkout" and cart_service and session_id:
                from database.db_service import OrderService
                order_service = OrderService()
                
                checkout_result = order_processor.process_checkout_request(
                    session_id=session_id,
                    cart_service=cart_service,
                    order_service=order_service
                )
                
                return {
                    "response": str(checkout_result.get("message", "")) if checkout_result and checkout_result.get("message") is not None else "",
                    "intent": str(intent) if intent is not None else "checkout",
                    "agent": str(get_agent_name(intent)) if get_agent_name(intent) is not None else "Checkout Specialist",
                    "sources": [],
                    "context": "",
                    "products": [],
                    "metadata": {"checkout_data": checkout_result.get("data", {}) if checkout_result else {}},
                    "chat_history_used": False,
                    "product_context_used": False,
                    "order_processing": {
                        "has_checkout_action": True,
                        "checkout_result": checkout_result
                    }
                }
            
            # Step 2c: Handle confirmation responses (product clarifications, not cart additions)
            if intent == "confirmation" and session_id:
                # For confirmations, we want to continue the sales conversation with context
                # This handles cases like "yes" when choosing between product options
                intent = "sales"  # Treat as sales intent but with confirmation context
                
            # Step 2d: Handle payment method selection
            if intent == "payment_method" and cart_service and session_id:
                from database.db_service import OrderService
                from .llm_utils import extract_payment_method
                
                order_service = OrderService()
                payment_method = extract_payment_method(query)
                
                checkout_result = order_processor.process_checkout_request(
                    session_id=session_id,
                    payment_method=payment_method,
                    cart_service=cart_service,
                    order_service=order_service
                )
                
                return {
                    "response": str(checkout_result.get("message", "")) if checkout_result and checkout_result.get("message") is not None else "",
                    "intent": str(intent) if intent is not None else "payment_method",
                    "agent": str(get_agent_name(intent)) if get_agent_name(intent) is not None else "Payment Specialist",
                    "sources": [],
                    "context": "",
                    "products": [],
                    "metadata": {"checkout_data": checkout_result.get("data", {}) if checkout_result else {}},
                    "chat_history_used": False,
                    "product_context_used": False,
                    "order_processing": {
                        "has_payment_action": True,
                        "payment_method": str(payment_method) if payment_method is not None else "",
                        "checkout_result": checkout_result
                    }
                }
            
            # Step 3: Intelligent decision on whether to use chat history
            use_chat_history = should_use_chat_history(query, intent)
            
            # Step 4: Intelligent decision on whether to resolve product context
            use_product_resolution = should_resolve_product_context(query, intent)
            
            # Step 5: Retrieve relevant documents
            retrieved_docs = self.retrieve_relevant_documents(query)
            
            # Step 6: Get chat history context (only if needed)
            chat_context = ""
            if use_chat_history:
                chat_context = get_chat_history_context(chat_history)
            
            # Step 7: Resolve product references (only if needed)
            product_context = ""
            if use_product_resolution:
                product_context = resolve_product_reference(query, chat_history)
            
            # Step 8: Format context
            formatted_context = format_rag_context(
                retrieved_docs, 
                chat_context, 
                product_context
            )
            
            # Step 9: Get specialized prompt based on intent
            specialized_prompt = get_specialized_prompt(intent, formatted_context, query)
            
            # Step 10: Generate response using specialized agent
            response = self._call_llm_with_prompt(specialized_prompt)
            
            # Step 11: Process order actions first (if this is an order-taking intent)
            order_processing_result = {"has_order_action": False}
            cart_action_happened = False
            
            if intent in ["order_taking", "sales"] and session_id and cart_service:
                # Extract order intent from the response
                order_actions = order_processor.extract_order_intent_from_response(response)
                
                if order_actions["has_order_action"]:
                    # Process the cart action with user_id
                    cart_result = order_processor.process_cart_action(
                        session_id, order_actions, cart_service, user_id
                    )
                    
                    order_processing_result = {
                        "has_order_action": True,
                        "action_type": order_actions["action_type"],
                        "cart_result": cart_result,
                        "items_processed": order_actions["items"]
                    }
                    
                    cart_action_happened = True
                    
                    # For successful cart actions, replace the response with a clean cart-focused message
                    if cart_result["success"]:
                        # Get updated cart summary with user_id
                        updated_cart = order_processor.get_cart_summary(session_id, cart_service, user_id)
                        
                        # Create a clean, cart-focused response
                        response = f"✅ **{cart_result['message']}**"
                        
                        if not updated_cart.get("empty", True):
                            response += f"\n\n{updated_cart['formatted_summary']}"
                        
                        response += "\n\n🛒 **What's next?**"
                        response += "\n- Say 'checkout' to place your order"
                        response += "\n- Ask for more products to continue shopping"
                        response += "\n- Say 'remove [item]' to modify your cart"
                    
                    elif order_actions["action_type"] == "suggest_add_to_cart":
                        # Add confirmation prompt for suggested items
                        response += "\n\n🛒 Would you like me to add this to your cart? Just say 'yes' or 'add it'!"

            # Step 12: Format response with structured product information
            formatted_response = {"products": [], "metadata": {}}
            try:
                if intent in ["sales", "general"] and not cart_action_happened:
                    # Only extract product recommendations when not handling cart actions
                    formatted_response = format_sales_response(response, intent, product_service)
                    logger.info(f"Extracted {len(formatted_response.get('products', []))} products for sales/general intent")
                elif cart_action_happened and order_processing_result.get("has_order_action"):
                    # For cart actions, include the processed items as products
                    processed_items = order_processing_result.get("items_processed", [])
                    cart_products = []
                    
                    # Convert processed items to product format
                    for item in processed_items:
                        if product_service:
                            try:
                                product_details = product_service.get_product_by_id(item["product_id"])
                                if product_details:
                                    cart_products.append({
                                        "id": item["product_id"],
                                        "name": product_details.get("name", "Unknown Product"),
                                        "quantity": item.get("quantity", 1),
                                        "size": item.get("size", ""),
                                        "price": product_details.get("price", 0),
                                        "action": order_processing_result.get("action_type", "unknown")
                                    })
                            except Exception as e:
                                logger.error(f"Error getting product details for ID {item['product_id']}: {e}")
                                # Fallback to basic info
                                cart_products.append({
                                    "id": item["product_id"],
                                    "name": f"Product {item['product_id']}",
                                    "quantity": item.get("quantity", 1),
                                    "size": item.get("size", ""),
                                    "action": order_processing_result.get("action_type", "unknown")
                                })
                    
                    formatted_response = {
                        "products": cart_products,
                        "metadata": {
                            "cart_action": True,
                            "action_type": order_processing_result.get("action_type", "unknown")
                        }
                    }
                    logger.info(f"Cart action detected - included {len(cart_products)} processed items as products")
                else:
                    # For non-sales intents, no product extraction needed
                    formatted_response = {"products": [], "metadata": {}}
            except Exception as e:
                logger.error(f"Error formatting response with product information: {e}")
                formatted_response = {"products": [], "metadata": {}}
            
            # Step 13: Get agent name
            agent_name = get_agent_name(intent)
            
            # Return structured response with order processing info
            return {
                "response": str(response) if response is not None else "",
                "intent": str(intent) if intent is not None else "general",
                "agent": str(agent_name) if agent_name is not None else "BrewMaster Assistant",
                "sources": retrieved_docs if retrieved_docs is not None else [],
                "context": str(formatted_context) if formatted_context is not None else "",
                "products": formatted_response.get("products", []),
                "metadata": formatted_response.get("metadata", {}),
                "chat_history_used": use_chat_history,
                "product_context_used": use_product_resolution,
                "order_processing": order_processing_result
            }
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again.",
                "intent": "error",
                "agent": "System",
                "sources": [],
                "context": "",
                "products": [],
                "metadata": {},
                "chat_history_used": False,
                "product_context_used": False,
                "order_processing": {"has_order_action": False, "error": str(e)}
            }
    def _call_llm_with_prompt(self, prompt: str) -> str:
        """Call the configured LLM provider with custom prompt"""
        if self.llm_provider == "local":
            return call_local_llm("", "", custom_prompt=prompt)
        elif self.llm_provider == "openai":
            return call_openai_llm("", "", custom_prompt=prompt)
        elif self.llm_provider == "gemini":
            return call_gemini_llm("", "", custom_prompt=prompt)
        else:
            return call_llm("", "", provider=self.llm_provider, custom_prompt=prompt)
    
    def _call_llm(self, context: str, query: str) -> str:
        """Call the configured LLM provider"""
        if self.llm_provider == "local":
            return call_local_llm(context, query)
        elif self.llm_provider == "openai":
            return call_openai_llm(context, query)
        elif self.llm_provider == "gemini":
            return call_gemini_llm(context, query)
        else:
            return call_llm(context, query, provider=self.llm_provider)


# Convenience functions for direct usage
def create_rag_system(llm_provider: str = "local") -> RAGSystem:
    """Create and return a RAG system instance"""
    return RAGSystem(llm_provider=llm_provider)


def quick_rag_query(query: str, llm_provider: str = "local") -> str:
    """
    Quick RAG query without advanced features.
    
    Args:
        query: User query
        llm_provider: LLM provider to use
        
    Returns:
        Response string
    """
    rag_system = RAGSystem(llm_provider=llm_provider)
    result = rag_system.generate_response(query)
    return result["response"]


def advanced_rag_query(
    query: str,
    chat_history: Optional[List[Dict[str, str]]] = None,
    llm_provider: str = "local"
) -> Dict[str, Any]:
    """
    Advanced RAG query with multi-agent system using intelligent context decisions.
    
    Args:
        query: User query
        chat_history: Previous conversation history
        llm_provider: LLM provider to use
        
    Returns:
        Complete response dictionary with agent information
    """
    rag_system = RAGSystem(llm_provider=llm_provider)
    return rag_system.generate_response(
        query,
        chat_history=chat_history
    )

