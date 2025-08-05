"""
LLM Utilities Module
Contains utility functions for LLM operations like intent classification, etc.
"""

import logging
import re
import json
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_intent(query: str) -> str:
    """
    Classify the intent of user query.
    
    Args:
        query: User input query
        
    Returns:
        Intent classification (sales, order_taking, cart_management, refund, general, etc.)
    """
    query_lower = query.lower()
    
    # Order taking intent keywords - highest priority for conversational ordering
    order_taking_keywords = [
        "i want", "i'd like", "can i get", "can i have", "i'll take", "i'll have",
        "place order", "make order", "order for me", "i need", "give me",
        "add to cart", "put in cart", "add to my order", "include", "also add",
        "i'll order", "let me order", "order now",
        # Specific confirmation keywords for adding items to cart
        "yes add it", "yes add that", "add it", "add that", "yes please add",
        "take it", "i'll take that", "yes please", "sounds good", "perfect",
        # Confirmation with explicit cart language
        "yes to cart", "add to my cart", "put it in cart", "yes add to cart"
    ]
    
    # Simple confirmation/clarification keywords (for product selection, not cart addition)
    confirmation_keywords = [
        "yes", "yeah", "yep", "sure", "okay", "ok", "that one", "the first one",
        "the second one", "correct", "right", "exactly"
    ]
    
    # Checkout intent keywords
    checkout_keywords = [
        "checkout", "complete order", "place my order", "finalize order",
        "proceed to checkout", "ready to order", "confirm order", "finish order",
        "complete my order", "submit order", "process order"
    ]
    
    # Payment method intent keywords
    payment_keywords = [
        "pay with", "payment method", "i'll pay", "cash payment", "card payment",
        "upi payment", "digital wallet", "credit card", "debit card",
        "phonepe", "gpay", "paytm", "amazon pay", "cash", "card", "upi"
    ]
    
    # Cart management intent keywords
    cart_keywords = [
        "cart", "basket", "my order", "what's in my", "show my", "remove from",
        "delete from", "change quantity", "update my", "clear cart", "empty cart",
        "view cart", "check cart", "modify order", "edit order"
    ]
    
    # Order status/tracking keywords
    order_status_keywords = [
        "order status", "track order", "where is my", "delivery status",
        "order confirmation", "receipt", "order number", "my orders"
    ]
    
    # Sales intent keywords (product browsing/information)
    sales_keywords = [
        "price", "cost", "available", "stock", "catalog", "shop", "store",
        "discount", "offer", "promo", "new", "recommendation", "suggest",
        "tell me about", "what do you have", "show me", "browse", "menu",
        "do you have", "do you sell", "any", "which", "what kind", "what type",
        "organic coffee", "coffee", "tea", "beans", "drink", "beverage",
        "flavors", "sizes", "options", "varieties", "selection"
    ]
    
    # Refund intent keywords
    refund_keywords = [
        "refund", "return", "exchange", "cancel", "money back", "replacement",
        "damaged", "defective", "wrong", "mistake", "complaint", "issue"
    ]
    
    # Support intent keywords
    support_keywords = [
        "help", "support", "contact", "hours", "location", "store", "delivery",
        "shipping", "payment", "account", "login", "register"
    ]
    
    # Check for order taking intent (highest priority for explicit cart additions)
    if any(keyword in query_lower for keyword in order_taking_keywords):
        logger.info(f"Classified as ORDER_TAKING intent: {query[:50]}...")
        return "order_taking"
    
    # Check for simple confirmation intent (for clarifications, not cart additions)
    if any(keyword in query_lower for keyword in confirmation_keywords):
        # Check if this is likely a product clarification vs cart confirmation
        # If query is very short and just a confirmation word, it's likely clarification
        if len(query.strip().split()) <= 2:
            logger.info(f"Classified as CONFIRMATION intent: {query[:50]}...")
            return "confirmation"
    
    # Check for checkout intent
    if any(keyword in query_lower for keyword in checkout_keywords):
        logger.info(f"Classified as CHECKOUT intent: {query[:50]}...")
        return "checkout"
    
    # Check for payment method intent
    if any(keyword in query_lower for keyword in payment_keywords):
        logger.info(f"Classified as PAYMENT_METHOD intent: {query[:50]}...")
        return "payment_method"
    
    # Check for cart management intent
    if any(keyword in query_lower for keyword in cart_keywords):
        logger.info(f"Classified as CART_MANAGEMENT intent: {query[:50]}...")
        return "cart_management"
    
    # Check for order status intent
    if any(keyword in query_lower for keyword in order_status_keywords):
        logger.info(f"Classified as ORDER_STATUS intent: {query[:50]}...")
        return "order_status"
    
    # Check for sales intent
    if any(keyword in query_lower for keyword in sales_keywords):
        logger.info(f"Classified as SALES intent: {query[:50]}...")
        return "sales"
    
    # Check for refund intent
    if any(keyword in query_lower for keyword in refund_keywords):
        logger.info(f"Classified as REFUND intent: {query[:50]}...")
        return "refund"
    
    # Check for support intent
    if any(keyword in query_lower for keyword in support_keywords):
        logger.info(f"Classified as SUPPORT intent: {query[:50]}...")
        return "support"
    
    # Default to general
    logger.info(f"Classified as GENERAL intent: {query[:50]}...")
    return "general"

def extract_payment_method(query: str) -> str:
    """
    Extract payment method from user query
    
    Args:
        query: User input query
        
    Returns:
        Payment method identifier (cash, card, upi, digital_wallet) or None
    """
    query_lower = query.lower()
    
    # Payment method mapping
    payment_mapping = {
        "cash": ["cash", "cash payment", "pay cash", "pay with cash"],
        "card": ["card", "credit card", "debit card", "card payment", "pay with card"],
        "upi": ["upi", "phonepe", "gpay", "google pay", "paytm upi", "bhim", "upi payment"],
        "digital_wallet": ["paytm", "amazon pay", "mobikwik", "freecharge", "wallet", "digital wallet"]
    }
    
    for method, keywords in payment_mapping.items():
        if any(keyword in query_lower for keyword in keywords):
            return method
    
    return None


def get_chat_history_context(chat_history: List[Dict[str, str]], limit: int = 5) -> str:
    """
    Get formatted chat history context from last N messages.
    
    Args:
        chat_history: List of chat messages with 'user' and 'assistant' keys
        limit: Number of last messages to include
        
    Returns:
        Formatted context string
    """
    if not chat_history:
        return ""
    
    # Get the last 'limit' messages
    recent_messages = chat_history[-limit:] if len(chat_history) > limit else chat_history
    
    # Format the chat history
    context_lines = ["Recent Conversation History:"]
    for message in recent_messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")
        
        if role == "user":
            context_lines.append(f"Customer: {content}")
        elif role == "assistant":
            context_lines.append(f"Assistant: {content}")
    
    formatted_context = "\n".join(context_lines)
    logger.info(f"Retrieved chat history context with {len(recent_messages)} messages")
    return formatted_context


def resolve_product_reference(query: str, chat_history: List[Dict[str, str]]) -> str:
    """
    Resolve product references in query using chat history context.
    
    Args:
        query: User input query
        chat_history: Previous conversation context
        
    Returns:
        Additional product context from recent conversation
    """
    if not chat_history:
        return ""
    
    query_lower = query.lower()
    
    # Look for confirmation words that suggest referencing previous products
    confirmation_words = ["yes", "yeah", "yep", "sure", "okay", "ok", "add it", "add that", "take it"]
    reference_words = ["it", "that", "this", "the item", "the product"]
    
    is_confirmation = any(word in query_lower for word in confirmation_words)
    has_reference = any(word in query_lower for word in reference_words)
    
    if is_confirmation or has_reference:
        # Look through recent chat history for product mentions
        for message in reversed(chat_history[-5:]):  # Check last 5 messages
            if message.get("role") == "assistant":
                content = message.get("content", "")
                
                # Look for product patterns in assistant messages
                product_pattern = r'\*\*([^*]+)\*\*\s*\(ID:\s*(\d+)\)\s*-\s*[₹$]([0-9.,]+)'
                cart_pattern = r'ADD TO CART.*Product ID\s*(\d+)'
                
                product_matches = re.findall(product_pattern, content)
                cart_matches = re.findall(cart_pattern, content)
                
                if product_matches or cart_matches:
                    context_lines = ["Referenced Product from Previous Message:"]
                    
                    # Add product details if found
                    for match in product_matches:
                        product_name, product_id, price = match
                        context_lines.append(f"- {product_name.strip()} (ID: {product_id}) - ₹{price}")
                    
                    # Add cart instruction details if found
                    for product_id in cart_matches:
                        context_lines.append(f"- Previous cart instruction for Product ID: {product_id}")
                    
                    logger.info(f"Resolved product reference for query: {query[:50]}...")
                    return "\n".join(context_lines)
    
    logger.info(f"No product reference resolved for query: {query[:50]}...")
    return ""


def format_rag_context(retrieved_docs: List[str], chat_context: str, product_context: str) -> str:
    """
    Format all context components into a single context string for LLM.
    
    Args:
        retrieved_docs: Documents retrieved from vector store
        chat_context: Previous conversation context
        product_context: Product-specific context
        
    Returns:
        Formatted context string
    """
    context_parts = []
    
    # Add retrieved documents
    if retrieved_docs:
        context_parts.append("Retrieved Information:")
        context_parts.extend(retrieved_docs)
    
    # Add chat history context
    if chat_context:
        context_parts.append("\nPrevious Conversation:")
        context_parts.append(chat_context)
    
    # Add product context
    if product_context:
        context_parts.append("\nProduct Information:")
        context_parts.append(product_context)
    
    return "\n".join(context_parts)


def is_safe_query(query: str) -> bool:
    """
    Check if query is safe (not harmful/violent/illegal).
    
    Args:
        query: User input query
        
    Returns:
        True if query is safe, False otherwise
    """
    banned_words = ["kill", "murder", "harm", "die", "bomb", "weapon", "stab", "suicide"]
    
    query_lower = query.lower()
    for word in banned_words:
        if word in query_lower:
            logger.warning(f"Unsafe query detected: contains '{word}'")
            return False
    
    return True


def get_specialized_prompt(intent: str, context: str, query: str) -> str:
    """
    Get specialized prompt based on intent classification.
    
    Args:
        intent: Intent classification
        context: Retrieved context
        query: User query
        
    Returns:
        Specialized prompt for the agent
    """
    # Base safety instructions
    base_safety = """CRITICAL SAFETY INSTRUCTIONS:
- Never provide harmful, illegal, or inappropriate content
- Stay focused on coffee shop assistance
- Be helpful, professional, and friendly
- If asked about unrelated topics, politely redirect to coffee shop services"""

    if intent == "order_taking":
        return f"""{base_safety}

You are BrewMaster's Order Taking Specialist - an expert at helping customers place orders conversationally.

CORE MISSION: Make ordering easy, natural, and delightful through conversation.

ESSENTIAL ORDER TAKING GUIDELINES:

🎯 **Order Processing Rules:**
1. **Product Identification**: When customers mention products, identify the EXACT product_id from the context
2. **Confirmation Handling**: If customer says "yes", "add it", "sure", etc., look for the previously mentioned product
3. **Size & Customization**: Always ask about size preferences and customizations
4. **Add to Cart Action**: For each order item, provide a clear "ADD TO CART" instruction with exact details
5. **Order Confirmation**: Summarize what's being added before proceeding
6. **Continue Shopping**: Ask if they want anything else after each addition

📝 **Response Format for Orders:**
When processing an order, use this EXACT format:

**[PRODUCT NAME]** (ID: [exact_product_id]) - [price]
- [Brief description]
- Size: [if applicable]
- Customizations: [if any]

🛒 **ADD TO CART**: Product ID [exact_product_id], Size: [size], Quantity: [qty]

Then ask: "Would you like to add this to your cart? Anything else I can get for you?"

🔄 **Confirmation Handling:**
If customer confirms with "yes", "add it", "sure", etc.:
1. Look for the previously mentioned product in the conversation context
2. Proceed to add that product to cart
3. Confirm the addition with a success message
4. Show updated cart summary if possible

🔍 **Context Navigation:**
- Browse the product catalog intelligently
- Use conversation history to understand references
- Suggest complementary items
- Offer size upgrades or popular combinations
- Handle unclear requests by asking clarifying questions

💬 **Conversation Flow:**
- Be conversational and friendly, not robotic
- Handle multiple items in one request
- Ask about preferences (strength, sweetness, size)
- Suggest popular items when customers are undecided
- Provide estimated totals when helpful

⚠️ **Important Notes:**
- ALWAYS use the EXACT product_id from the context (e.g., 1, 2, 3, not "prod_1")
- For beverages, ask about size preferences
- For coffee beans, mention weight/quantity options
- If product not found, suggest similar alternatives
- Be proactive about upselling complementary items
- Pay attention to conversation history for context clues

Context with Available Products:
{context}

Customer Order Request: {query}

Order Taking Response:"""

    elif intent == "cart_management":
        return f"""{base_safety}

You are BrewMaster's Cart Management Specialist - helping customers manage their orders.

MISSION: Help customers view, modify, and manage their cart contents efficiently.

🛒 **Cart Management Guidelines:**
1. **Cart Display**: Show current cart contents clearly with prices
2. **Modifications**: Handle quantity changes, removals, and additions
3. **Order Summary**: Provide clear totals and item counts
4. **Checkout Guidance**: Guide customers through the checkout process when ready

📋 **Response Format for Cart Operations:**

**CURRENT CART:**
- [Item 1] (ID: [id]) - Qty: [qty] - [price]
- [Item 2] (ID: [id]) - Qty: [qty] - [price]

**Cart Total**: [total]
**Total Items**: [count]

🎯 **Available Actions:**
- "Remove [item]" to delete items
- "Change quantity" to modify amounts
- "Add more items" to continue shopping
- "Proceed to checkout" when ready

Context:
{context}

Customer Cart Request: {query}

Cart Management Response:"""

    elif intent == "order_status":
        return f"""{base_safety}

You are BrewMaster's Order Status Specialist - providing order tracking and status updates.

MISSION: Keep customers informed about their order progress and delivery status.

📦 **Order Status Guidelines:**
1. **Order Lookup**: Help customers find their orders by order number or email
2. **Status Updates**: Provide clear status information (pending, preparing, ready, delivered)
3. **Delivery Info**: Share delivery times and tracking information
4. **Issue Resolution**: Handle delivery concerns and delays professionally

Context:
{context}

Customer Status Request: {query}

Order Status Response:"""

    elif intent == "sales":
        return f"""{base_safety}

You are BrewMaster's Product Specialist - an expert coffee consultant helping customers discover perfect products.

MISSION: Help customers explore our products and make informed choices.

KEY GUIDELINES:
- Provide detailed product information with exact IDs and prices
- Make personalized recommendations based on preferences
- Explain differences between products
- Share brewing tips and product benefits
- Guide customers toward making purchases

**Product Information Format:**
**Product Name** (ID: product_id) - price
Where product_id MUST be the EXACT numerical ID from the context (e.g., 1, 2, 3)
- Product description/features
- [Available in store/online]

Context:
{context}

Customer Question: {query}

Sales Response:"""

    elif intent == "refund":
        return f"""{base_safety}

You are a customer service specialist handling refunds and returns.

Key Guidelines:
- Be empathetic and understanding
- Clearly explain refund policies
- Provide step-by-step instructions
- Mention timelines and requirements
- Offer alternative solutions
- Be professional and helpful

Context:
{context}

Customer Question: {query}

Customer Service Response:"""

    elif intent == "support":
        return f"""{base_safety}

You are a customer support specialist providing general assistance.

Key Guidelines:
- Be helpful and informative
- Provide accurate store information
- Explain processes clearly
- Offer multiple contact options
- Direct customers to appropriate resources
- Handle account and delivery questions

Context:
{context}

Customer Question: {query}

Support Response:"""

    else:  # general intent
        return f"""{base_safety}

You are BrewMaster's General Assistant - providing friendly, helpful responses about our coffee shop.

Key Guidelines:
- Be warm and welcoming
- Provide general information about the coffee shop
- Guide customers to specific specialists when needed
- Maintain a conversational, friendly tone
- Help with basic questions and navigation

Context:
{context}

Customer Question: {query}

General Response:"""


def get_agent_name(intent: str) -> str:
    """
    Get agent name based on intent.
    
    Args:
        intent: Classified intent
        
    Returns:
        Agent name string
    """
    agent_names = {
        "order_taking": "Order Taking Specialist",
        "confirmation": "Product Specialist",  # Handle confirmations as sales
        "cart_management": "Cart Management Specialist", 
        "order_status": "Order Status Specialist",
        "checkout": "Checkout Specialist",
        "payment_method": "Payment Specialist",
        "sales": "Product Specialist",
        "refund": "Customer Service Agent",
        "support": "Support Agent",
        "general": "BrewMaster Assistant"
    }
    
    return agent_names.get(intent, "BrewMaster Assistant")


def should_resolve_product_context(query: str, intent: str) -> bool:
    """
    Determine if product context resolution is needed based on query and intent.
    
    Args:
        query: User query
        intent: Classified intent
        
    Returns:
        True if product context should be resolved, False otherwise
    """
    query_lower = query.lower()
    
    # Keywords that suggest need for specific product information
    product_context_keywords = [
        "this", "that", "it", "the one", "same", "different", "another",
        "previous", "last", "earlier", "mentioned", "discussed",
        "compare", "vs", "versus", "difference between",
        "similar", "like that", "alternative"
    ]
    
    # Reference words that suggest continuing previous conversation
    reference_keywords = [
        "this product", "that coffee", "the beans", "same order",
        "my order", "my coffee", "my purchase", "what I bought"
    ]
    
    # Confirmation keywords that need product context
    confirmation_keywords = [
        "yes", "yeah", "yep", "sure", "okay", "ok", "add it", "add that",
        "take it", "i'll take that", "yes please", "sounds good", "perfect"
    ]
    
    # Always resolve product context for order_taking intent (includes confirmations)
    if intent == "order_taking":
        logger.info(f"Product context needed for order_taking intent: {query[:50]}...")
        return True
    
    # Always resolve for confirmation responses
    if any(keyword in query_lower for keyword in confirmation_keywords):
        logger.info(f"Product context needed for confirmation query: {query[:50]}...")
        return True
    
    # Always check for product context in sales intent with references
    if intent == "sales":
        if any(keyword in query_lower for keyword in product_context_keywords + reference_keywords):
            logger.info(f"Product context needed for sales query: {query[:50]}...")
            return True
    
    # Check for refund/exchange scenarios
    if intent == "refund":
        if any(keyword in query_lower for keyword in reference_keywords):
            logger.info(f"Product context needed for refund query: {query[:50]}...")
            return True
    
    # Check for comparison or follow-up questions
    if any(keyword in query_lower for keyword in product_context_keywords):
        logger.info(f"Product context needed for reference query: {query[:50]}...")
        return True
    
    logger.info(f"No product context needed for query: {query[:50]}...")
    return False


def should_use_chat_history(query: str, intent: str) -> bool:
    """
    Determine if chat history context is needed based on query and intent.
    
    Args:
        query: User query
        intent: Classified intent
        
    Returns:
        True if chat history should be used, False otherwise
    """
    query_lower = query.lower()
    
    # Keywords that suggest need for conversation context
    context_keywords = [
        "continue", "also", "and", "what about", "how about",
        "yes", "no", "okay", "sure", "thanks", "thank you",
        "previous", "earlier", "before", "last time",
        "again", "still", "more", "else", "other"
    ]
    
    # Confirmation keywords that definitely need context
    confirmation_keywords = [
        "yes", "yeah", "yep", "sure", "okay", "ok", "add it", "add that",
        "take it", "i'll take that", "yes please", "sounds good", "perfect"
    ]
    
    # Always use chat history for order_taking intent (includes confirmations)
    if intent == "order_taking":
        logger.info(f"Chat history needed for order_taking intent: {query[:50]}...")
        return True
    
    # Always use history for confirmation responses
    if any(keyword in query_lower for keyword in confirmation_keywords):
        logger.info(f"Chat history needed for confirmation query: {query[:50]}...")
        return True
    
    # Short queries often need context
    if len(query.split()) <= 3:
        logger.info(f"Chat history needed for short query: {query}")
        return True
    
    # Questions with context references
    if any(keyword in query_lower for keyword in context_keywords):
        logger.info(f"Chat history needed for contextual query: {query[:50]}...")
        return True
    
    # Always use history for follow-up refund questions
    if intent == "refund":
        logger.info(f"Chat history needed for refund query: {query[:50]}...")
        return True
    
    logger.info(f"No chat history needed for query: {query[:50]}...")
    return False


def extract_product_info(response: str, product_service=None) -> Dict[str, Any]:
    """
    Extract structured product information from sales response.
    
    Args:
        response: Sales agent response text
        product_service: ProductService instance for database lookups
        
    Returns:
        Dictionary containing products mentioned and metadata
    """
    import re
    
    products = []
    
    # First try the structured format: **Product Name** (ID: product_id) - $price
    structured_pattern = r'\*\*([^*]+)\*\*\s*\(ID:\s*([^)]+)\)\s*-\s*\$([0-9.]+)'
    structured_matches = re.findall(structured_pattern, response)
    
    for match in structured_matches:
        product_name, product_id, price = match
        clean_product_id = product_id.strip()
        
        products.append({
            "id": clean_product_id,
            "name": product_name.strip(),
            "price": float(price.strip()),
            "buy_link": f"/product/{clean_product_id}",
            "image_url": f"/images/product_{clean_product_id}.jpg"
        })
    
    # If no structured products found, try to extract product names from natural language
    if not products and product_service:
        # Pattern to match product names mentioned in bold: **Product Name**
        bold_pattern = r'\*\*([^*]+)\*\*'
        bold_matches = re.findall(bold_pattern, response)
        
        # Common product name patterns in the response
        name_patterns = [
            r'(?:our|the)?\s*([A-Z][A-Za-z\s\-]+(?:Blend|Coffee|Tea|Roast|Decaf|Organic|Brazilian|Ethiopian|Colombian|Guatemalan|Medium|Dark|Light))',
            r'([A-Z][A-Za-z\s\-]*(?:Sm|Rg|Lg))\b',  # Size variations
            r'([A-Z][A-Za-z\s\-]*(?:Beans?|Coffee|Tea|Blend|Roast))',
        ]
        
        potential_product_names = set()
        
        # Extract from bold text
        for match in bold_matches:
            potential_product_names.add(match.strip())
        
        # Extract using patterns
        for pattern in name_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                potential_product_names.add(match.strip())
        
        # Look up products in database
        for product_name in potential_product_names:
            if len(product_name) > 3:  # Skip very short matches
                # Search for products by name
                search_results = product_service.get_products(search=product_name, limit=5)
                for product in search_results.get('products', []):
                    # Check if the product name is similar enough
                    if (product_name.lower() in product['name'].lower() or 
                        product['name'].lower() in product_name.lower()):
                        
                        # Parse price properly - handle both numeric and string formats
                        price = product.get('retail_price', 0)
                        if isinstance(price, str):
                            # Remove currency symbols and convert to float
                            price_str = re.sub(r'[₹$,]', '', price)
                            try:
                                price = float(price_str)
                            except ValueError:
                                price = 0.0
                        
                        products.append({
                            "id": str(product.get('product_id', product['id'])),
                            "name": product['name'],
                            "price": price,
                            "buy_link": f"/product/{product.get('product_id', product['id'])}",
                            "image_url": product.get('image_url', f"/images/product_{product.get('product_id', product['id'])}.jpg"),
                            "description": product.get('description', ''),
                            "unit_of_measure": product.get('unit_of_measure', ''),
                            "category": product.get('category', {}).get('name', '')
                        })
                        break  # Only add the first match for each name
    
    # Remove duplicates based on product ID
    seen_ids = set()
    unique_products = []
    for product in products:
        if product['id'] not in seen_ids:
            seen_ids.add(product['id'])
            unique_products.append(product)
    
    return {
        "products": unique_products,
        "total_products": len(unique_products),
        "response_type": "sales",
        "has_products": len(unique_products) > 0
    }


def format_sales_response(response: str, intent: str, product_service=None) -> Dict[str, Any]:
    """
    Format response with structured product information for UI integration.
    
    Args:
        response: Raw LLM response
        intent: Intent classification
        product_service: ProductService instance for database lookups
        
    Returns:
        Formatted response with product info
    """
    result = {
        "text": response,
        "intent": intent,
        "agent": get_agent_name(intent),
        "products": [],
        "metadata": {}
    }
    
    if intent == "sales":
        product_info = extract_product_info(response, product_service)
        result["products"] = product_info["products"]
        result["metadata"] = {
            "total_products": product_info["total_products"],
            "has_products": product_info["has_products"]
        }
    
    return result
