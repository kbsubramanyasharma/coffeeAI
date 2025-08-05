#!/usr/bin/env python3
"""
CSV to SQLite Database Migration Script
Migrates product.csv data to the coffee shop database
"""

import sqlite3
import csv
import json
import os
from pathlib import Path
from decimal import Decimal
import re

class DatabaseMigrator:
    def __init__(self, db_path="coffee_shop.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {self.db_path}")
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
            
    def create_schema(self):
        """Create database schema"""
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r') as f:
            schema = f.read()
            
        self.cursor.executescript(schema)
        self.conn.commit()
        print("Database schema created")
        
    def clean_price(self, price_str):
        """Clean and convert price string to decimal"""
        if not price_str:
            return 0.0
            
        # Remove currency symbols and whitespace
        cleaned = re.sub(r'[^\d.]', '', str(price_str))
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
            
    def get_category_id(self, product_group, product_category, product_type):
        """Get category ID based on product classification"""
        # Map CSV categories to database categories
        category_mapping = {
            'Whole Bean/Teas': {
                'Coffee beans': 6,
                'Loose Tea': 7,
                'Packaged Chocolate': 8
            },
            'Beverages': {
                'Coffee': 9,
                'Tea': 10,
                'Drinking Chocolate': 11
            },
            'Food': {
                'Bakery': 12
            },
            'Merchandise': {
                'Branded': 13
            },
            'Add-ons': {
                'Flavours': 14
            }
        }
        
        return category_mapping.get(product_group, {}).get(product_category, 1)
        
    def get_product_type_id(self, product_type):
        """Get product type ID based on product type name"""
        type_mapping = {
            'Organic Beans': 1,
            'House blend Beans': 2,
            'Espresso Beans': 3,
            'Gourmet Beans': 4,
            'Premium Beans': 5,
            'Green beans': 6,
            'Herbal tea': 7,
            'Black tea': 8,
            'Green tea': 9,
            'Chai tea': 10,
            'Drinking Chocolate': 11,
            'Organic Chocolate': 12,
            'Drip coffee': 13,
            'Organic brewed coffee': 14,
            'Gourmet brewed coffee': 15,
            'Premium brewed coffee': 16,
            'Barista Espresso': 17,
            'Seasonal drink': 18,
            'Specialty coffee': 19,
            'Brewed herbal tea': 20,
            'Brewed Green tea': 21,
            'Brewed Black tea': 22,
            'Brewed Chai tea': 23,
            'Hot chocolate': 24,
            'Pastry': 26,
            'Scone': 27,
            'Biscotti': 28,
            'Clothing': 29,
            'Housewares': 30,
            'Regular syrup': 31,
            'Sugar free syrup': 32
        }
        
        return type_mapping.get(product_type, 1)
        
    def get_product_group_id(self, product_group):
        """Get product group ID"""
        group_mapping = {
            'Whole Bean/Teas': 1,
            'Beverages': 2,
            'Food': 3,
            'Merchandise': 4,
            'Add-ons': 5
        }
        
        return group_mapping.get(product_group, 1)
        
    def generate_image_url(self, product_name, product_type):
        """Generate specific image URLs based on product type"""
        
        # Map product types to real Unsplash coffee images
        image_mapping = {
            # Coffee Bean Products
            'Organic Beans': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop',
            'House blend Beans': 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=400&h=300&fit=crop',
            'Espresso Beans': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400&h=300&fit=crop',
            'Gourmet Beans': 'https://images.unsplash.com/photo-1587734195503-904fca47e0df?w=400&h=300&fit=crop',
            'Premium Beans': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop',
            'Green beans': 'https://images.unsplash.com/photo-1587734195480-d8c86d652543?w=400&h=300&fit=crop',
            
            # Coffee Beverages
            'Drip coffee': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop',
            'Organic brewed coffee': 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400&h=300&fit=crop',
            'Gourmet brewed coffee': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop',
            'Premium brewed coffee': 'https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop',
            'Barista Espresso': 'https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400&h=300&fit=crop',
            'Specialty coffee': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=300&fit=crop',
            'Seasonal drink': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop',
            
            # Tea Products
            'Herbal tea': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop',
            'Black tea': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop',
            'Green tea': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop',
            'Chai tea': 'https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=400&h=300&fit=crop',
            'Brewed herbal tea': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop',
            'Brewed Green tea': 'https://images.unsplash.com/photo-1564890273409-06d1dda0d66e?w=400&h=300&fit=crop',
            'Brewed Black tea': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop',
            'Brewed Chai tea': 'https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=400&h=300&fit=crop',
            'Loose Tea': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop',
            
            # Chocolate Products
            'Drinking Chocolate': 'https://images.unsplash.com/photo-1542990253-0b8be0849d8d?w=400&h=300&fit=crop',
            'Organic Chocolate': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop',
            'Hot chocolate': 'https://images.unsplash.com/photo-1542990253-0b8be0849d8d?w=400&h=300&fit=crop',
            'Packaged Chocolate': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop',
            
            # Food Items
            'Pastry': 'https://images.unsplash.com/photo-1559620192-032c4bc4674d?w=400&h=300&fit=crop',
            'Scone': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop',
            'Biscotti': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop',
            
            # Merchandise
            'Clothing': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',
            'Housewares': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop',
            
            # Syrups and Add-ons
            'Regular syrup': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop',
            'Sugar free syrup': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop',
        }
        
        # Try to find exact match first
        if product_type in image_mapping:
            return image_mapping[product_type]
        
        # Try to find partial matches based on keywords
        product_lower = product_type.lower()
        name_lower = product_name.lower()
        
        if 'espresso' in product_lower or 'espresso' in name_lower:
            return image_mapping.get('Barista Espresso', image_mapping['Drip coffee'])
        elif 'tea' in product_lower and 'chai' in product_lower:
            return image_mapping['Chai tea']
        elif 'tea' in product_lower and 'green' in product_lower:
            return image_mapping['Green tea']
        elif 'tea' in product_lower and 'black' in product_lower:
            return image_mapping['Black tea']
        elif 'tea' in product_lower:
            return image_mapping['Herbal tea']
        elif 'chocolate' in product_lower or 'cocoa' in product_lower:
            return image_mapping['Hot chocolate']
        elif 'bean' in product_lower:
            return image_mapping['House blend Beans']
        elif 'coffee' in product_lower:
            return image_mapping['Drip coffee']
        elif 'pastry' in product_lower or 'cake' in product_lower:
            return image_mapping['Pastry']
        elif 'syrup' in product_lower:
            return image_mapping['Regular syrup']
        
        # Default fallback
        return image_mapping['Drip coffee']
        
    def generate_nutrition_info(self, product_name, product_type):
        """Generate placeholder nutrition info"""
        nutrition_templates = {
            'Coffee': {
                'calories': 5,
                'caffeine': '95mg',
                'fat': '0g',
                'carbs': '1g',
                'protein': '0g',
                'sugar': '0g'
            },
            'Tea': {
                'calories': 2,
                'caffeine': '30mg',
                'fat': '0g',
                'carbs': '0g',
                'protein': '0g',
                'sugar': '0g'
            },
            'Bakery': {
                'calories': 250,
                'caffeine': '0mg',
                'fat': '12g',
                'carbs': '35g',
                'protein': '5g',
                'sugar': '15g'
            },
            'Chocolate': {
                'calories': 150,
                'caffeine': '10mg',
                'fat': '8g',
                'carbs': '20g',
                'protein': '3g',
                'sugar': '18g'
            }
        }
        
        # Determine nutrition template
        if 'coffee' in product_type.lower():
            template = nutrition_templates['Coffee']
        elif 'tea' in product_type.lower():
            template = nutrition_templates['Tea']
        elif 'chocolate' in product_type.lower():
            template = nutrition_templates['Chocolate']
        elif any(word in product_type.lower() for word in ['pastry', 'scone', 'biscotti']):
            template = nutrition_templates['Bakery']
        else:
            template = nutrition_templates['Coffee']
            
        return json.dumps(template)
        
    def migrate_products(self, csv_path):
        """Migrate products from CSV to database"""
        print(f"Migrating products from {csv_path}...")
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Clean and prepare data
                    product_id = int(row['product_id'])
                    name = row['product'].strip()
                    description = row['product_description'].strip()
                    product_group = row['product_group'].strip()
                    product_category = row['product_category'].strip()
                    product_type = row['product_type'].strip()
                    unit_of_measure = row['unit_of_measure'].strip()
                    
                    # Clean prices
                    wholesale_price = self.clean_price(row['current_wholesale_price'])
                    retail_price = self.clean_price(row['current_retail_price'])
                    
                    # Convert Y/N to boolean
                    tax_exempt = row['tax_exempt_yn'].upper() == 'Y'
                    is_promo = row['promo_yn'].upper() == 'Y'
                    is_new = row['new_product_yn'].upper() == 'Y'
                    
                    # Get IDs
                    category_id = self.get_category_id(product_group, product_category, product_type)
                    product_type_id = self.get_product_type_id(product_type)
                    product_group_id = self.get_product_group_id(product_group)
                    
                    # Generate additional data
                    image_url = self.generate_image_url(name, product_type)
                    nutrition_info = self.generate_nutrition_info(name, product_type)
                    
                    # Determine if product is popular (based on price and type)
                    is_popular = retail_price > 15.0 or 'espresso' in name.lower() or 'premium' in product_type.lower()
                    
                    # Generate rating (placeholder)
                    rating = round(4.0 + (retail_price / 50.0), 1)  # Higher price = slightly higher rating
                    rating = min(5.0, max(3.5, rating))  # Keep between 3.5 and 5.0
                    
                    # Insert product
                    self.cursor.execute("""
                        INSERT OR REPLACE INTO products (
                            product_id, name, description, product_group_id, category_id, 
                            product_type_id, unit_of_measure, wholesale_price, retail_price,
                            tax_exempt, is_promo, is_new, is_active, is_popular, image_url,
                            rating, nutrition_info, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """, (
                        product_id, name, description, product_group_id, category_id,
                        product_type_id, unit_of_measure, wholesale_price, retail_price,
                        tax_exempt, is_promo, is_new, True, is_popular, image_url,
                        rating, nutrition_info
                    ))
                    
                except Exception as e:
                    print(f"Error migrating product {row.get('product_id', 'unknown')}: {e}")
                    continue
                    
        self.conn.commit()
        print("Products migration completed")
        
    def create_sample_user(self):
        """Create a sample user for testing"""
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (
                    email, password_hash, first_name, last_name, is_active, is_admin
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                'admin@coffeeai.com',
                'hashed_password_here',  # In production, use proper password hashing
                'Admin',
                'User',
                True,
                True
            ))
            self.conn.commit()
            print("Sample user created")
        except Exception as e:
            print(f"Error creating sample user: {e}")
            
    def run_migration(self, csv_path):
        """Run complete migration process"""
        try:
            print("Starting CSV to Database Migration...")
            
            # Connect to database
            self.connect()
            
            # Create schema
            self.create_schema()
            
            # Migrate products
            self.migrate_products(csv_path)
            
            # Create sample user
            self.create_sample_user()
            
            # Verify migration
            self.cursor.execute("SELECT COUNT(*) FROM products")
            product_count = self.cursor.fetchone()[0]
            print(f"Migration completed! {product_count} products imported")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            raise
        finally:
            self.close()


def main():
    """Main migration function"""
    # Get CSV file path
    csv_path = Path(__file__).parent.parent / "chatbot_rag-main" / "product.csv"
    
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return
        
    # Create database directory if it doesn't exist
    db_dir = Path(__file__).parent
    db_dir.mkdir(exist_ok=True)
    
    # Run migration
    migrator = DatabaseMigrator(db_path=str(db_dir / "coffee_shop.db"))
    migrator.run_migration(str(csv_path))
    
    print("\nMigration completed successfully!")
    print(f"Database location: {db_dir / 'coffee_shop.db'}")
    print("\nYou can now use the database with your application!")


if __name__ == "__main__":
    main()
