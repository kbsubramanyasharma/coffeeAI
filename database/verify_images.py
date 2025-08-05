#!/usr/bin/env python3
"""
Verification script for product images
Shows the distribution and statistics of product images
"""

import sqlite3

def verify_images():
    """Verify image assignment and show statistics"""
    try:
        conn = sqlite3.connect('coffee_shop.db')
        cursor = conn.cursor()
        
        # Get total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        
        # Get products with images
        cursor.execute("SELECT COUNT(*) FROM products WHERE image_url IS NOT NULL")
        products_with_images = cursor.fetchone()[0]
        
        # Get unique images
        cursor.execute("SELECT COUNT(DISTINCT image_url) FROM products WHERE image_url IS NOT NULL")
        unique_images = cursor.fetchone()[0]
        
        # Get image distribution
        cursor.execute("""
            SELECT image_url, COUNT(*) as count 
            FROM products 
            WHERE image_url IS NOT NULL 
            GROUP BY image_url 
            ORDER BY count DESC 
            LIMIT 10
        """)
        image_distribution = cursor.fetchall()
        
        # Get some sample products
        cursor.execute("""
            SELECT id, name, image_url 
            FROM products 
            WHERE image_url IS NOT NULL 
            ORDER BY id 
            LIMIT 10
        """)
        sample_products = cursor.fetchall()
        
        print("🖼️  PRODUCT IMAGES VERIFICATION REPORT")
        print("=" * 50)
        print(f"📊 Statistics:")
        print(f"   Total Products: {total_products}")
        print(f"   Products with Images: {products_with_images}")
        print(f"   Unique Images: {unique_images}")
        print(f"   Coverage: {products_with_images/total_products*100:.1f}%")
        print(f"   Uniqueness: {unique_images/products_with_images*100:.1f}%")
        
        print(f"\n📈 Image Distribution (Top 10):")
        for i, (image_url, count) in enumerate(image_distribution, 1):
            short_url = image_url.split('/')[-1][:30] + "..." if len(image_url) > 30 else image_url.split('/')[-1]
            print(f"   {i:2d}. {short_url} - Used by {count} product(s)")
        
        print(f"\n🎯 Sample Products:")
        for product_id, name, image_url in sample_products:
            short_name = name[:35] + "..." if len(name) > 35 else name
            image_id = image_url.split('/')[-1].split('?')[0][:20]
            print(f"   ID {product_id:3d}: {short_name:<38} -> {image_id}")
        
        print(f"\n✅ Image assignment verification completed successfully!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    verify_images()
