#!/usr/bin/env python3
"""
Order Processing Module for Chat-based Ordering
Handles conversational order taking, cart management, and order completion
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class OrderItem:
    """Represents an item in the order"""
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    size: Optional[str] = None
    customizations: Optional[Dict[str, Any]] = None

@dataclass
class ChatOrder:
    """Represents an order being built through chat"""
    session_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "building"  # building, ready_for_checkout, completed
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class OrderProcessor:
    """Handles conversational order processing"""
    
    def __init__(self, db_service=None):
        self.db_service = db_service
        self.active_orders = {}  # session_id -> ChatOrder
        
    def extract_order_intent_from_response(self, response: str) -> Dict[str, Any]:
        """
        Extract order instructions from LLM response
        
        Args:
            response: LLM response text
            
        Returns:
            Dictionary containing order actions
        """
        result = {
            "has_order_action": False,
            "action_type": None,  # "add_to_cart", "remove_from_cart", "modify_quantity"
            "items": [],
            "instructions": []
        }
        
        # Pattern to match ADD TO CART instructions (with emoji)
        add_to_cart_pattern = r'🛒\s*\*\*ADD TO CART\*\*:\s*Product ID\s*(\d+)(?:,\s*Size:\s*([^,]+))?(?:,\s*Quantity:\s*(\d+))?'
        
        # Alternative pattern without emoji
        add_to_cart_alt_pattern = r'ADD TO CART:\s*Product ID\s*(\d+)(?:,\s*Size:\s*([^,]+))?(?:,\s*Quantity:\s*(\d+))?'
        
        # Pattern to match product mentions with IDs
        product_pattern = r'\*\*([^*]+)\*\*\s*\(ID:\s*(\d+)\)\s*-\s*[₹$]([0-9.,]+)'
        
        # Look for ADD TO CART instructions (primary pattern)
        add_matches = re.findall(add_to_cart_pattern, response, re.IGNORECASE)
        if not add_matches:
            add_matches = re.findall(add_to_cart_alt_pattern, response, re.IGNORECASE)
        
        for match in add_matches:
            product_id, size, quantity = match
            result["has_order_action"] = True
            result["action_type"] = "add_to_cart"
            
            item_data = {
                "product_id": int(product_id),
                "quantity": int(quantity) if quantity else 1,
                "size": size.strip() if size else None
            }
            result["items"].append(item_data)
            result["instructions"].append(f"Add Product ID {product_id} to cart")
        
        # If no explicit ADD TO CART, look for product mentions in order-taking responses
        if not result["has_order_action"]:
            product_matches = re.findall(product_pattern, response)
            
            # Check if this looks like an order confirmation or completion
            order_keywords = [
                "add to your cart", "would you like to add", "shall I add", "adding to cart",
                "successfully added", "added to cart", "item added", "order confirmed",
                "perfect! adding", "great choice! adding", "excellent! i'll add"
            ]
            is_order_context = any(keyword in response.lower() for keyword in order_keywords)
            
            # Also check for confirmation responses
            confirmation_keywords = [
                "yes, i'll add", "absolutely! adding", "sure thing! adding",
                "coming right up", "perfect choice", "great selection"
            ]
            is_confirmation = any(keyword in response.lower() for keyword in confirmation_keywords)
            
            if product_matches and (is_order_context or is_confirmation):
                result["has_order_action"] = True
                result["action_type"] = "suggest_add_to_cart"
                
                for match in product_matches:
                    product_name, product_id, price = match
                    item_data = {
                        "product_id": int(product_id),
                        "product_name": product_name.strip(),
                        "price": float(price.replace(',', '')),
                        "quantity": 1
                    }
                    result["items"].append(item_data)
        
        return result
    
    def process_cart_action(self, session_id: str, action_data: Dict[str, Any], 
                           cart_service=None, user_id: int = None) -> Dict[str, Any]:
        """
        Process cart actions extracted from chat
        
        Args:
            session_id: User session ID
            action_data: Action data from extract_order_intent_from_response
            cart_service: Cart service instance
            user_id: User ID for cart operations
            
        Returns:
            Result of the cart operation
        """
        result = {
            "success": False,
            "message": "",
            "cart_updated": False,
            "items_added": []
        }
        
        if not action_data["has_order_action"] or not cart_service:
            return result
        
        try:
            for item in action_data["items"]:
                # Add item to cart using the cart service with user_id
                cart_result = cart_service.add_to_cart(
                    session_id=session_id,
                    product_id=item["product_id"],
                    quantity=item.get("quantity", 1),
                    selected_size=item.get("size"),
                    user_id=user_id
                )
                
                if cart_result:
                    result["items_added"].append({
                        "product_id": item["product_id"],
                        "quantity": item.get("quantity", 1),
                        "size": item.get("size")
                    })
                    result["cart_updated"] = True
            
            if result["cart_updated"]:
                result["success"] = True
                result["message"] = f"Successfully added {len(result['items_added'])} item(s) to your cart!"
            else:
                result["message"] = "No items were added to the cart."
                
        except Exception as e:
            logger.error(f"Error processing cart action: {e}")
            result["message"] = f"Sorry, there was an error adding items to your cart: {str(e)}"
        
        return result
    
    def get_cart_summary(self, session_id: str, cart_service=None, user_id: int = None) -> Dict[str, Any]:
        """
        Get formatted cart summary for chat responses
        
        Args:
            session_id: User session ID
            cart_service: Cart service instance
            user_id: User ID for cart operations
            
        Returns:
            Formatted cart information
        """
        if not cart_service:
            return {"error": "Cart service not available"}
        
        try:
            cart_data = cart_service.get_cart(session_id, user_id)
            
            if not cart_data or not cart_data.get("items"):
                return {
                    "empty": True,
                    "message": "Your cart is currently empty. Would you like to browse our menu?",
                    "item_count": 0,
                    "total": 0
                }
            
            # Format cart items for display
            formatted_items = []
            for item in cart_data["items"]:
                # Handle both old and new cart data structures
                product_name = "Unknown"
                if "product" in item and item["product"]:
                    product_name = item["product"].get("name", "Unknown")
                elif "product_name" in item:
                    product_name = item.get("product_name", "Unknown")
                
                formatted_items.append({
                    "name": product_name,
                    "id": item["product_id"],
                    "quantity": item["quantity"],
                    "size": item.get("selected_size", "Regular"),
                    "price": item["total_price"]
                })
            
            return {
                "empty": False,
                "items": formatted_items,
                "item_count": cart_data.get("total_items", 0),
                "total": cart_data.get("total_amount", 0),
                "formatted_summary": self._format_cart_for_chat(
                    formatted_items, 
                    cart_data.get("total_amount", 0),
                    cart_data.get("total_items", 0)  # Pass total quantity
                )
            }
            
        except Exception as e:
            logger.error(f"Error getting cart summary: {e}")
            return {"error": f"Error retrieving cart: {str(e)}"}
    
    def _format_cart_for_chat(self, items: List[Dict], total: float, total_quantity: int = None) -> str:
        """Format cart items for chat display"""
        if not items:
            return "Your cart is empty."
        
        lines = ["**CURRENT CART:**"]
        for item in items:
            size_info = f" ({item['size']})" if item['size'] and item['size'] != 'Regular' else ""
            lines.append(f"- {item['name']}{size_info} - Qty: {item['quantity']} - ₹{item['price']:.2f}")
        
        lines.append(f"\n**Cart Total**: ₹{total:.2f}")
        
        # Use total_quantity if provided, otherwise calculate from items
        if total_quantity is not None:
            lines.append(f"**Total Items**: {total_quantity}")
        else:
            # Fallback: sum quantities of all items
            total_qty = sum(item['quantity'] for item in items)
            lines.append(f"**Total Items**: {total_qty}")
        
        return "\n".join(lines)
    
    def suggest_complementary_items(self, current_items: List[Dict], 
                                  product_service=None) -> List[Dict]:
        """
        Suggest complementary items based on current cart contents
        
        Args:
            current_items: Current cart items
            product_service: Product service instance
            
        Returns:
            List of suggested products
        """
        suggestions = []
        
        if not product_service or not current_items:
            return suggestions
        
        try:
            # Simple complementary logic
            has_coffee = any("coffee" in item.get("name", "").lower() for item in current_items)
            has_pastry = any(any(food_type in item.get("name", "").lower() 
                               for food_type in ["scone", "croissant", "pastry"]) 
                           for item in current_items)
            
            # Suggest pastries if they have coffee
            if has_coffee and not has_pastry:
                # Get some pastry items
                pastry_products = product_service.get_products(
                    search="scone", limit=2
                )
                if pastry_products and pastry_products.get("products"):
                    suggestions.extend(pastry_products["products"][:2])
            
            # Suggest coffee if they have pastries but no coffee
            if has_pastry and not has_coffee:
                coffee_products = product_service.get_products(
                    search="latte", limit=2
                )
                if coffee_products and coffee_products.get("products"):
                    suggestions.extend(coffee_products["products"][:2])
                    
        except Exception as e:
            logger.error(f"Error suggesting complementary items: {e}")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def create_checkout_summary(self, session_id: str, cart_service=None) -> Dict[str, Any]:
        """
        Create a checkout summary for order completion
        
        Args:
            session_id: User session ID
            cart_service: Cart service instance
            
        Returns:
            Checkout summary data
        """
        cart_summary = self.get_cart_summary(session_id, cart_service)
        
        if cart_summary.get("empty", True):
            return {
                "ready_for_checkout": False,
                "message": "Your cart is empty. Add some items before checkout!"
            }
        
        # Calculate taxes and fees (simplified)
        subtotal = cart_summary["total"]
        tax_rate = 0.18  # 18% GST
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        return {
            "ready_for_checkout": True,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "item_count": cart_summary["item_count"],
            "items": cart_summary["items"],
            "checkout_message": f"""
**ORDER SUMMARY**
Subtotal: ₹{subtotal:.2f}
Tax (18%): ₹{tax_amount:.2f}
**Total: ₹{total_amount:.2f}**

Items: {cart_summary['item_count']}

Ready to place your order? Just say "checkout" or "place order" and I'll guide you through the payment process!
"""
        }
    
    def save_chat_order_to_database(self, session_id: str, payment_method: str, 
                                   user_id: int = None, cart_service=None, 
                                   order_service=None, notes: str = None) -> Dict[str, Any]:
        """
        Save a chat-based order to the database with payment method
        
        Args:
            session_id: User session ID
            payment_method: Payment method (cash, card, upi, wallet)
            user_id: User ID (optional for guest orders)
            cart_service: Cart service instance
            order_service: Order service instance
            notes: Additional order notes
            
        Returns:
            Order creation result
        """
        result = {
            "success": False,
            "message": "",
            "order_id": None,
            "order_number": None
        }
        
        if not cart_service or not order_service:
            result["message"] = "Required services not available"
            return result
        
        try:
            # Get cart data - need to pass user_id to get_cart method
            cart_data = cart_service.get_cart(session_id, user_id)
            
            if not cart_data or not cart_data.get("items"):
                result["message"] = "Cart is empty. Cannot create order."
                return result
            
            # Calculate order totals - use correct field names
            subtotal = cart_data["total_amount"]  # The actual field from get_cart
            tax_rate = 0.18  # 18% GST
            tax_amount = subtotal * tax_rate
            total_amount = subtotal + tax_amount
            
            # Prepare order items for database
            order_items = []
            for item in cart_data["items"]:
                order_items.append({
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"],
                    "total_price": item["total_price"],
                    "selected_size": item.get("selected_size"),
                    "customizations": item.get("customizations"),
                    "notes": item.get("notes")
                })
            
            # Create order data
            order_data = {
                "user_id": user_id,
                "session_id": session_id,
                "status": "confirmed",  # Chat orders are pre-confirmed
                "total_amount": subtotal,
                "tax_amount": tax_amount,
                "discount_amount": 0,
                "final_amount": total_amount,
                "payment_status": "pending",
                "payment_method": payment_method,
                "notes": f"Chat Order - {notes}" if notes else "Chat Order",
                "order_items": order_items
            }
            
            # Create order in database
            created_order = order_service.create_order(order_data)
            
            if created_order:
                result["success"] = True
                result["order_id"] = created_order["id"]
                result["order_number"] = created_order["order_number"]
                result["message"] = f"Order {created_order['order_number']} created successfully!"
                
                # Clear the cart after successful order creation - pass user_id
                cart_service.clear_cart(session_id, user_id)
                
            else:
                result["message"] = "Failed to create order in database"
                
        except Exception as e:
            logger.error(f"Error saving chat order to database: {e}")
            result["message"] = f"Error creating order: {str(e)}"
        
        return result
    
    def get_available_payment_methods(self) -> List[Dict[str, str]]:
        """
        Get list of available payment methods
        
        Returns:
            List of payment method options
        """
        return [
            {"id": "cash", "name": "Cash Payment", "description": "Pay with cash at pickup/delivery"},
            {"id": "card", "name": "Card Payment", "description": "Credit/Debit card payment"},
            {"id": "upi", "name": "UPI Payment", "description": "Pay via UPI (PhonePe, GPay, Paytm)"},
            {"id": "digital_wallet", "name": "Digital Wallet", "description": "Paytm, Amazon Pay, etc."}
        ]
    
    def process_checkout_request(self, session_id: str, payment_method: str = None, 
                               user_id: int = None, cart_service=None, 
                               order_service=None) -> Dict[str, Any]:
        """
        Process a checkout request from chat
        
        Args:
            session_id: User session ID
            payment_method: Selected payment method
            user_id: User ID (optional)
            cart_service: Cart service instance
            order_service: Order service instance
            
        Returns:
            Checkout processing result
        """
        result = {
            "checkout_stage": "summary",  # summary, payment_method, confirm, completed
            "message": "",
            "data": {}
        }
        
        # Get checkout summary
        checkout_summary = self.create_checkout_summary(session_id, cart_service)
        
        if not checkout_summary.get("ready_for_checkout"):
            result["message"] = checkout_summary.get("message", "Cart is empty")
            return result
        
        # If no payment method specified, show options
        if not payment_method:
            result["checkout_stage"] = "payment_method"
            result["data"]["checkout_summary"] = checkout_summary
            result["data"]["payment_methods"] = self.get_available_payment_methods()
            result["message"] = f"""
{checkout_summary['checkout_message']}

**PAYMENT OPTIONS:**
1. 💵 Cash Payment - Pay at pickup/delivery
2. 💳 Card Payment - Credit/Debit card
3. 📱 UPI Payment - PhonePe, GPay, Paytm
4. 💰 Digital Wallet - Paytm, Amazon Pay

Please choose your payment method by saying something like:
"I'll pay with cash" or "UPI payment" or "Card payment"
"""
            return result
        
        # Validate payment method
        valid_methods = [pm["id"] for pm in self.get_available_payment_methods()]
        if payment_method not in valid_methods:
            result["message"] = f"Invalid payment method. Please choose from: {', '.join(valid_methods)}"
            return result
        
        # Process the order
        order_result = self.save_chat_order_to_database(
            session_id=session_id,
            payment_method=payment_method,
            user_id=user_id,
            cart_service=cart_service,
            order_service=order_service,
            notes="Conversational Order via Chat"
        )
        
        if order_result["success"]:
            result["checkout_stage"] = "completed"
            result["data"]["order"] = order_result
            payment_method_name = next(
                (pm["name"] for pm in self.get_available_payment_methods() if pm["id"] == payment_method),
                payment_method
            )
            result["message"] = f"""
🎉 **ORDER CONFIRMED!**

**Order Number:** {order_result['order_number']}
**Payment Method:** {payment_method_name}
**Total Amount:** ₹{checkout_summary['total_amount']:.2f}

Your order has been successfully placed! 

For cash payment: Have the exact amount ready at pickup/delivery
For card/UPI: You'll receive payment instructions shortly
For digital wallet: Check your app for payment request

Thank you for your order! ☕️
"""
        else:
            result["message"] = f"Sorry, there was an error processing your order: {order_result['message']}"
        
        return result

# Global instance for easy access
order_processor = OrderProcessor()
