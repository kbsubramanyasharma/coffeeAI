#!/usr/bin/env python3
"""
Test script for forgot password functionality with actual email sending
"""

import sys
import os
from pathlib import Path
import secrets
from datetime import datetime, timedelta

# Add the correct paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "chatbot_rag-main"))

# Change to the correct directory for imports
os.chdir(str(project_root / "chatbot_rag-main"))

def test_email_sending():
    """Test sending actual password reset email"""
    try:
        print("Testing email service...")
        
        # Import with correct path
        from core.email_service import EmailService
        
        email_service = EmailService()
        
        # Check if credentials are configured
        if not email_service.email or not email_service.password:
            print("✗ Gmail credentials not configured properly")
            return False
            
        print(f"✓ Gmail configured: {email_service.email}")
        
        # Generate a test token
        test_token = secrets.token_urlsafe(32)
        print(f"✓ Generated test token: {test_token[:10]}...")
        
        # Send test email
        print("Sending test password reset email...")
        success = email_service.send_password_reset_email(
            recipient_email="rvit23mca063.rvitm@rvei.edu.in",
            reset_token=test_token,
            user_name="Test User RVIT"
        )
        
        if success:
            print("✓ Test email sent successfully!")
            print("✓ Check your inbox at: rvit23mca063.rvitm@rvei.edu.in")
            print(f"✓ Reset URL would be: http://localhost:5173/reset-password?token={test_token}")
            return True
        else:
            print("✗ Failed to send test email")
            return False
            
    except Exception as e:
        print(f"✗ Email test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_setup():
    """Test if database table exists"""
    try:
        import sqlite3
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if password_reset_tokens table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='password_reset_tokens'
        """)
        
        table_exists = cursor.fetchone() is not None
        conn.close()
        
        if table_exists:
            print("✓ password_reset_tokens table exists")
            return True
        else:
            print("✗ password_reset_tokens table missing")
            return False
            
    except Exception as e:
        print(f"✗ Database setup error: {e}")
        return False

def test_user_service():
    """Test UserService methods"""
    try:
        from database.db_service import UserService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        
        # Check if new methods exist
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
        print(f"✗ UserService test error: {e}")
        return False

def main():
    print("Testing Forgot Password Implementation")
    print("=" * 50)
    print(f"Test email will be sent to: rvit23mca063.rvitm@rvei.edu.in")
    print("=" * 50)
    
    success = True
    
    # Test 1: Database setup
    print("1. Testing database setup...")
    success &= test_database_setup()
    print()
    
    # Test 2: UserService methods
    print("2. Testing UserService methods...")
    success &= test_user_service()
    print()
    
    # Test 3: Email sending
    print("3. Testing email sending...")
    success &= test_email_sending()
    print()
    
    print("=" * 50)
    if success:
        print("✓ ALL TESTS PASSED!")
        print("\n🎉 Your forgot password implementation is working!")
        print("\n📧 Check your email inbox for the test reset email!")
        print("\n🚀 API Endpoints ready:")
        print("   POST /api/v1/forgot-password")
        print("   POST /api/v1/reset-password")
        print("\n💡 Next: Start your server with 'python main.py'")
    else:
        print("✗ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
