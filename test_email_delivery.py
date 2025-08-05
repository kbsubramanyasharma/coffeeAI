#!/usr/bin/env python3
"""
Test forgot password with RVIT email to confirm it works
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

def create_rvit_user_and_test():
    """Create RVIT user and test forgot password"""
    try:
        from database.db_service import UserService
        from core.email_service import EmailService
        import hashlib
        import secrets as sec
        
        def hash_password(password: str) -> str:
            salt = sec.token_hex(16)
            hash_obj = hashlib.sha256((password + salt).encode())
            return f"{salt}${hash_obj.hexdigest()}"
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        email_service = EmailService()
        
        test_email = "rvit23mca063.rvitm@rvei.edu.in"
        
        # Check if user exists, if not create
        user = user_service.get_user_by_email(test_email)
        
        if not user:
            print(f"Creating RVIT user: {test_email}")
            user_data = {
                'name': 'RVIT Test User',
                'email': test_email,
                'password_hash': hash_password('testpassword123'),
                'phone': None
            }
            user = user_service.create_user(user_data)
            print("✓ RVIT user created!")
        else:
            print("✓ RVIT user already exists")
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
        
        # Store token
        success = user_service.create_password_reset_token(user["id"], reset_token, expires_at)
        if not success:
            print("✗ Failed to create reset token")
            return False
        
        print("✓ Reset token created")
        
        # Send email
        email_sent = email_service.send_password_reset_email(
            recipient_email=test_email,
            reset_token=reset_token,
            user_name="RVIT Test User"
        )
        
        if email_sent:
            print("✓ Email sent to RVIT email successfully!")
            print(f"✓ Token: {reset_token}")
            return True
        else:
            print("✗ Failed to send email")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gmail_direct():
    """Test sending directly to Gmail"""
    try:
        from core.email_service import EmailService
        
        email_service = EmailService()
        
        # Generate test token
        test_token = secrets.token_urlsafe(32)
        
        print("Testing direct Gmail send...")
        success = email_service.send_password_reset_email(
            recipient_email="kbsubrhamanyasharma9632@gmail.com",
            reset_token=test_token,
            user_name="KB Subramanya Sharma"
        )
        
        if success:
            print("✓ Direct Gmail send successful!")
            print("  Check Gmail inbox, spam, and promotions tab")
            return True
        else:
            print("✗ Direct Gmail send failed")
            return False
            
    except Exception as e:
        print(f"✗ Direct Gmail error: {e}")
        return False

def main():
    print("Testing Forgot Password Email Delivery")
    print("=" * 50)
    
    # Test 1: Send to RVIT email (we know this works)
    print("1. Testing with RVIT email...")
    rvit_success = create_rvit_user_and_test()
    print()
    
    # Test 2: Send directly to Gmail
    print("2. Testing direct Gmail send...")
    gmail_success = test_gmail_direct()
    print()
    
    print("=" * 50)
    print("RESULTS:")
    print(f"RVIT Email: {'✓ Success' if rvit_success else '✗ Failed'}")
    print(f"Gmail Email: {'✓ Success' if gmail_success else '✗ Failed'}")
    
    if rvit_success and gmail_success:
        print("\n✅ Both emails sent successfully!")
        print("\n📧 Check these inboxes:")
        print("   - rvit23mca063.rvitm@rvei.edu.in")
        print("   - kbsubrhamanyasharma9632@gmail.com")
        print("\n💡 If Gmail email not received, check:")
        print("   - Spam/Junk folder")
        print("   - Promotions tab")
        print("   - All Mail folder")
        print("   - Wait 2-3 minutes for delivery")

if __name__ == "__main__":
    main()
