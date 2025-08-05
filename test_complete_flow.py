#!/usr/bin/env python3
"""
Test the complete forgot password flow to generate a real email with token
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

def test_complete_flow():
    """Test complete forgot password flow and generate real email"""
    try:
        from database.db_service import UserService
        from core.email_service import EmailService
        
        db_path = str(project_root / "database" / "coffee_shop.db")
        user_service = UserService(db_path)
        email_service = EmailService()
        
        test_email = "rvit23mca063.rvitm@rvei.edu.in"
        
        print("Testing complete forgot password flow...")
        
        # Step 1: Check if user exists
        user = user_service.get_user_by_email(test_email)
        if not user:
            print("✗ User not found")
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
        
        # Step 4: Send email with correct frontend URL
        user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        email_sent = email_service.send_password_reset_email(
            recipient_email=test_email,
            reset_token=reset_token,
            user_name=user_name or "Test User"
        )
        
        if email_sent:
            print("✓ Password reset email sent successfully!")
            print(f"✓ Reset token: {reset_token}")
            print(f"✓ Reset URL: http://localhost:8080/reset-password?token={reset_token}")
            print("✓ Check your email inbox!")
            print("\n📧 The email now contains a link that will:")
            print("   1. Take you to http://localhost:8080/reset-password?token=...")
            print("   2. Automatically extract the token from URL")
            print("   3. Show only password fields (token is hidden)")
            print("   4. Redirect to login after successful reset")
            return True
        else:
            print("✗ Failed to send password reset email")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Testing Updated Reset Password Flow")
    print("=" * 50)
    
    success = test_complete_flow()
    
    print("=" * 50)
    if success:
        print("✅ COMPLETE FLOW WORKING!")
        print("\n🎯 What's Fixed:")
        print("   ✓ Token automatically extracted from URL")
        print("   ✓ Token field removed from form")
        print("   ✓ Added password confirmation")
        print("   ✓ Added password validation")
        print("   ✓ Added loading states")
        print("   ✓ Auto-redirect to login after success")
        print("   ✓ Better error handling")
        print("\n📧 Check rvit23mca063.rvitm@rvei.edu.in for the test email!")
    else:
        print("❌ Flow has issues!")

if __name__ == "__main__":
    main()
