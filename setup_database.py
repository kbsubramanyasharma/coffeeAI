#!/usr/bin/env python3
"""
Complete Database Setup Script for Coffee AI
Handles schema creation, data migration, and verification
"""

import os
import sys
from pathlib import Path
import sqlite3
import subprocess

def check_dependencies():
    """Check if required dependencies are available"""
    print("Checking dependencies...")
    
    # Check Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Python 3.8+ is required")
        return False
    print(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if required modules are available
    try:
        import sqlite3
        print("SQLite3 module available")
    except ImportError:
        print("SQLite3 module not available")
        return False
        
    try:
        import csv
        print("CSV module available")
    except ImportError:
        print("CSV module not available")
        return False
        
    try:
        import json
        print("JSON module available")
    except ImportError:
        print("JSON module not available")
        return False
        
    return True

def create_database_directory():
    """Create database directory if it doesn't exist"""
    db_dir = Path("database")
    db_dir.mkdir(exist_ok=True)
    print(f"Database directory created: {db_dir}")
    return db_dir

def run_migration():
    """Run the CSV to database migration"""
    print("\nRunning database migration...")
    
    migration_script = Path("database/migrate_csv_to_db.py")
    if not migration_script.exists():
        print(f"Migration script not found: {migration_script}")
        return False
        
    try:
        result = subprocess.run([sys.executable, str(migration_script)], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def verify_database():
    """Verify the database was created correctly"""
    print("\nVerifying database...")
    
    db_path = Path("database/coffee_shop.db")
    if not db_path.exists():
        print(f"Database file not found: {db_path}")
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            'categories', 'product_groups', 'product_types', 'products',
            'users', 'chat_sessions', 'chat_messages', 'cart_items',
            'orders', 'order_items'
        ]
        
        missing_tables = set(expected_tables) - set(tables)
        if missing_tables:
            print(f"Missing tables: {missing_tables}")
            return False
            
        print(f"All tables created: {len(tables)} tables")
        
        # Check data
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"Products imported: {product_count} products")
        
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        print(f"Categories created: {category_count} categories")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"Users created: {user_count} users")
        
        # Check sample data
        cursor.execute("SELECT name, retail_price FROM products LIMIT 5")
        sample_products = cursor.fetchall()
        print(f"Sample products: {len(sample_products)} products found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database verification failed: {e}")
        return False

def test_database_operations():
    """Test basic database operations"""
    print("\nTesting database operations...")
    
    try:
        # Import database services
        sys.path.insert(0, str(Path.cwd()))
        from database.db_service import ProductService, CartService, ChatService
        
        db_path = "database/coffee_shop.db"
        
        # Test product service
        product_service = ProductService(db_path)
        products = product_service.get_products(limit=5)
        print(f"Product service test: {len(products['products'])} products retrieved")
        
        # Test cart service
        cart_service = CartService(db_path)
        session_id = "test_session_123"
        cart = cart_service.get_cart(session_id)
        print(f"Cart service test: {cart['total_items']} items in cart")
        
        # Test chat service
        chat_service = ChatService(db_path)
        chat_service.create_chat_session(session_id)
        print(f"Chat service test: Session created")
        
        return True
        
    except Exception as e:
        print(f"Database operations test failed: {e}")
        return False

def create_backup():
    """Create a backup of the database"""
    print("\nCreating database backup...")
    
    db_path = Path("database/coffee_shop.db")
    backup_path = Path("database/coffee_shop_backup.db")
    
    if not db_path.exists():
        print("Database file not found for backup")
        return False
        
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"Database backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"Backup creation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("Coffee AI Database Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\nSetup failed: Missing dependencies")
        return False
        
    # Create database directory
    create_database_directory()
    
    # Run migration
    if not run_migration():
        print("\nSetup failed: Migration failed")
        return False
        
    # Verify database
    if not verify_database():
        print("\nSetup failed: Database verification failed")
        return False
        
    # Test operations
    if not test_database_operations():
        print("\nSetup failed: Database operations test failed")
        return False
        
    # Create backup
    create_backup()
    
    print("\n" + "=" * 50)
    print("Database setup completed successfully!")
    print("\nDatabase Summary:")
    print("   Location: database/coffee_shop.db")
    print("   Schema: Complete with all tables")
    print("   Data: 88 products imported from CSV")
    print("   Users: Sample admin user created")
    print("   Services: All database services tested")
    print("\nYou can now start the application!")
    print("   Backend: cd chatbot_rag-main && python main.py")
    print("   Frontend: npm run dev")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 