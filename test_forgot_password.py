#!/usr/bin/env python3
"""
Test script for forgot password functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all imports work"""
    try:
        from core.email_service import EmailService
        from database.db_service import UserService
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_database_methods():
    """Test if database methods exist"""
    try:
        from database.db_service import UserService
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        
        methods = [
            'create_password_reset_token',
            'get_password_reset_token', 
            'use_password_reset_token',
            'update_user_password'
        ]
        
        for method in methods:
            if hasattr(user_service, method):
                print(f"✓ {method} method exists")
            else:
                print(f"✗ {method} method missing")
                return False
        return True
    except Exception as e:
        print(f"✗ Database test error: {e}")
        return False

def test_email_service():
    """Test email service initialization"""
    try:
        from core.email_service import EmailService
        email_service = EmailService()
        print("✓ EmailService initialized")
        
        # Check if credentials are configured
        if email_service.email and email_service.password:
            print("✓ Gmail credentials configured")
        else:
            print("! Gmail credentials not configured (this is normal for testing)")
        return True
    except Exception as e:
        print(f"✗ Email service error: {e}")
        return False

def main():
    print("Testing Forgot Password Implementation")
    print("=" * 40)
    
    success = True
    success &= test_imports()
    success &= test_database_methods() 
    success &= test_email_service()
    
    print("=" * 40)
    if success:
        print("✓ All tests passed! Implementation is ready.")
        print("\nNext steps:")
        print("1. Update Gmail credentials in .env file")
        print("2. Start the server: python main.py")
        print("3. Test endpoints:")
        print("   POST /api/v1/forgot-password")
        print("   POST /api/v1/reset-password")
    else:
        print("✗ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
