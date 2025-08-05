#!/usr/bin/env python3

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_service import CartService, ProductService
from chatbot_rag-main.core.order_processor import OrderProcessor

def test_cart_display():
    """Test cart display formatting"""
    
    # Sample cart data structure (simulating what cart_service.get_cart returns)
    mock_cart_data = {
        "items": [
            {
                "product_id": 8,
                "product": {"name": "Civet Cat"},
                "quantity": 1,
                "selected_size": ".5 lb",
                "total_price": 3757.50
            },
            {
                "product_id": 1,
                "product": {"name": "Brazilian - Organic"},
                "quantity": 2,
                "selected_size": ".5 lb", 
                "total_price": 3006.00
            }
        ],
        "total_items": 3,  # 1 + 2
        "total_amount": 6763.50
    }
    
    # Test the cart formatting
    processor = OrderProcessor()
    result = processor.get_cart_summary("test-session", None, 1)
    
    print("=== Cart Summary Test ===")
    print("Mock cart data:")
    print(f"- Civet Cat: qty=1, price=3757.50")
    print(f"- Brazilian: qty=2, price=3006.00")
    print(f"- Expected total items: 3")
    print(f"- Expected total amount: 6763.50")
    
    print("\nIf we had this cart, the display should show:")
    print("**CURRENT CART:**")
    print("- Civet Cat (.5 lb) - Qty: 1 - ₹3757.50")
    print("- Brazilian - Organic (.5 lb) - Qty: 2 - ₹3006.00")
    print("")
    print("**Cart Total**: ₹6763.50")
    print("**Total Items**: 3")

if __name__ == "__main__":
    test_cart_display()
