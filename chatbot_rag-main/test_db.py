#!/usr/bin/env python3

import sys
from pathlib import Path

# Add parent to path to import database service
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_service import ProductService, CartService

def test_products():
    # Check product in database
    db_path = str(Path(__file__).parent.parent / "database" / "coffee_shop.db")
    product_service = ProductService(db_path)
    
    print("Testing product database...")
    
    # Check if product ID 1 exists
    product = product_service.get_product_by_id(1)
    if product:
        print(f'Product ID 1: {product["name"]} - Price: {product["retail_price"]}')
    else:
        print('Product ID 1 not found')

    # Check if Civet Cat exists (should be product_id 8)
    product8 = product_service.get_product_by_id(8)
    if product8:
        print(f'Product ID 8: {product8["name"]} - Price: {product8["retail_price"]}')
    else:
        print('Product ID 8 not found')
    
    # Search for Civet Cat
    products = product_service.get_products(search='Civet Cat', limit=1)
    if products['products']:
        civet = products['products'][0]
        print(f'Civet Cat found: ID={civet["id"]}, Name={civet["name"]}, Price={civet["retail_price"]}')
    else:
        print('Civet Cat not found in search')

if __name__ == "__main__":
    test_products()
