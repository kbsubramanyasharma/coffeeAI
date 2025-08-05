#!/usr/bin/env python3
"""
Test script for forgot password functionality with actual email sending
"""

import sys
import os
from pathlib import Path
import sqlite3
from datetime import datetime, timedelta
import secrets

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "chatbot_rag-main"))

def test_email_sending():
    """Test sending actual password reset email"""
    try:
        # Import after adding to path
        from chatbot_rag_main.core.email_service import EmailService
        
        print("Testing email service...")
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
            user_name="Test User"
        )
        
        if success:
            print("✓ Test email sent successfully!")
            print("Check your inbox at: rvit23mca063.rvitm@rvei.edu.in")
            return True
        else:
            print("✗ Failed to send test email")
            return False
            
    except Exception as e:
        print(f"✗ Email test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_operations():
    """Test database operations for password reset"""
    try:
        # Import database service
        from chatbot_rag_main.database.db_service import UserService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        
        print("Testing database operations...")
        
        # Create test user if doesn't exist
        test_email = "rvit23mca063.rvitm@rvei.edu.in"
        existing_user = user_service.get_user_by_email(test_email)
        
        if not existing_user:
            print("Creating test user...")
            import hashlib
            import secrets
            
            def hash_password(password: str) -> str:
                salt = secrets.token_hex(16)
                hash_obj = hashlib.sha256((password + salt).encode())
                return f"{salt}${hash_obj.hexdigest()}"
            
            user_data = {
                'name': 'Test User RVIT',
                'email': test_email,
                'password_hash': hash_password('testpassword123'),
                'phone': None
            }
            
            user = user_service.create_user(user_data)
            print(f"✓ Created test user with ID: {user['id']}")
        else:
            user = existing_user
            print(f"✓ Using existing test user with ID: {user['id']}")
        
        # Test password reset token creation
        test_token = secrets.token_urlsafe(32)
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
        
        success = user_service.create_password_reset_token(user['id'], test_token, expires_at)
        if success:
            print("✓ Password reset token created successfully")
        else:
            print("✗ Failed to create password reset token")
            return False
        
        # Test token retrieval
        token_data = user_service.get_password_reset_token(test_token)
        if token_data:
            print("✓ Password reset token retrieved successfully")
            print(f"  Token expires at: {token_data['expires_at']}")
        else:
            print("✗ Failed to retrieve password reset token")
            return False
        
        print("✓ All database operations successful")
        return True
        
    except Exception as e:
        print(f"✗ Database test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_flow():
    """Test the complete forgot password flow"""
    try:
        print("Testing complete forgot password flow...")
        
        # Import services
        from chatbot_rag_main.core.email_service import EmailService
        from chatbot_rag_main.database.db_service import UserService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        email_service = EmailService()
        
        test_email = "rvit23mca063.rvitm@rvei.edu.in"
        
        # Step 1: Check if user exists
        user = user_service.get_user_by_email(test_email)
        if not user:
            print("✗ Test user not found")
            return False
        
        print(f"✓ Found user: {user['email']}")
        
        # Step 2: Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
        
        # Step 3: Store token
        success = user_service.create_password_reset_token(user["id"], reset_token, expires_at)
        if not success:
            print("✗ Failed to create reset token")
            return False
        
        print("✓ Reset token created and stored")
        
        # Step 4: Send email
        user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        email_sent = email_service.send_password_reset_email(
            recipient_email=test_email,
            reset_token=reset_token,
            user_name=user_name or "Test User"
        )
        
        if email_sent:
            print("✓ Password reset email sent successfully!")
            print(f"✓ Reset token: {reset_token}")
            print("✓ Check your email inbox!")
            return True
        else:
            print("✗ Failed to send password reset email")
            return False
            
    except Exception as e:
        print(f"✗ Full flow test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Testing Forgot Password Implementation")
    print("=" * 50)
    print(f"Test email will be sent to: rvit23mca063.rvitm@rvei.edu.in")
    print("=" * 50)
    
    # Test database operations first
    db_success = test_database_operations()
    print()
    
    # Test email sending
    email_success = test_email_sending()
    print()
    
    # Test complete flow
    flow_success = test_full_flow()
    
    print("=" * 50)
    if db_success and email_success and flow_success:
        print("✓ ALL TESTS PASSED!")
        print("\nYour forgot password implementation is working!")
        print("\nAPI Endpoints available:")
        print("- POST /api/v1/forgot-password")
        print("- POST /api/v1/reset-password")
        print("\nCheck your email for the reset link!")
    else:
        print("✗ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
