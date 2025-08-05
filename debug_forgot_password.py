#!/usr/bin/env python3
"""
Debug script for forgot password - check if user exists and test email sending
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

def check_user_exists():
    """Check if the user exists in database"""
    try:
        from database.db_service import UserService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        
        test_email = "kbsubrhamanyasharma9632@gmail.com"
        
        print(f"Checking if user exists: {test_email}")
        user = user_service.get_user_by_email(test_email)
        
        if user:
            print("✓ User found in database!")
            print(f"  User ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"  Active: {user.get('is_active', False)}")
            return user
        else:
            print("✗ User NOT found in database!")
            print("This is why you're not receiving the email.")
            return None
            
    except Exception as e:
        print(f"✗ Error checking user: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_test_user():
    """Create the test user if it doesn't exist"""
    try:
        from database.db_service import UserService
        import hashlib
        import secrets
        
        def hash_password(password: str) -> str:
            salt = secrets.token_hex(16)
            hash_obj = hashlib.sha256((password + salt).encode())
            return f"{salt}${hash_obj.hexdigest()}"
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        
        test_email = "kbsubrhamanyasharma9632@gmail.com"
        
        print(f"Creating user: {test_email}")
        
        user_data = {
            'name': 'KB Subramanya Sharma',
            'email': test_email,
            'password_hash': hash_password('defaultpassword123'),
            'phone': None
        }
        
        user = user_service.create_user(user_data)
        print("✓ User created successfully!")
        print(f"  User ID: {user['id']}")
        print(f"  Email: {user['email']}")
        return user
        
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_forgot_password_flow():
    """Test the complete forgot password flow for your email"""
    try:
        from database.db_service import UserService
        from core.email_service import EmailService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        email_service = EmailService()
        
        test_email = "kbsubrhamanyasharma9632@gmail.com"
        
        print(f"Testing forgot password flow for: {test_email}")
        
        # Step 1: Check if user exists
        user = user_service.get_user_by_email(test_email)
        if not user:
            print("✗ User not found - this is why email isn't sent!")
            return False
        
        print(f"✓ User found: {user['email']}")
        
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
            user_name=user_name or "KB Subramanya Sharma"
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
        print(f"✗ Forgot password flow error: {e}")
        import traceback
        traceback.print_exc()
        return False

def list_all_users():
    """List all users in the database"""
    try:
        from database.db_service import UserService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        
        # Get all users
        users = user_service.execute_query("SELECT id, email, first_name, last_name, is_active FROM users LIMIT 10")
        
        print("All users in database:")
        if users:
            for user in users:
                print(f"  ID: {user['id']}, Email: {user['email']}, Name: {user.get('first_name', '')} {user.get('last_name', '')}, Active: {user.get('is_active', False)}")
        else:
            print("  No users found in database!")
            
        return users
        
    except Exception as e:
        print(f"✗ Error listing users: {e}")
        return []

def main():
    print("Debugging Forgot Password Issue")
    print("=" * 50)
    print(f"Email trying to reset: kbsubrhamanyasharma9632@gmail.com")
    print("=" * 50)
    
    # Step 1: List all users
    print("1. Listing all users in database...")
    users = list_all_users()
    print()
    
    # Step 2: Check if specific user exists
    print("2. Checking if your email exists...")
    user = check_user_exists()
    print()
    
    # Step 3: Create user if doesn't exist
    if not user:
        print("3. Creating user since it doesn't exist...")
        user = create_test_user()
        print()
    
    # Step 4: Test forgot password flow
    if user:
        print("4. Testing forgot password flow...")
        success = test_forgot_password_flow()
        print()
        
        print("=" * 50)
        if success:
            print("✅ PROBLEM SOLVED!")
            print("Your user now exists and email should be sent!")
            print("Try the forgot password from frontend again.")
        else:
            print("❌ Still having issues - check the errors above.")
    else:
        print("❌ Could not create or find user.")

if __name__ == "__main__":
    main()
