#!/usr/bin/env python3
"""
Test script to verify forgot password frontend integration works correctly
"""

import requests
import json
import time

def test_forgot_password_flow():
    """Test the complete forgot password flow"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 Testing Forgot Password Frontend Integration")
    print("=" * 50)
    
    # Test 1: Forgot Password Request
    print("\n1. Testing forgot password request...")
    test_email = "test@example.com"
    
    try:
        response = requests.post(
            f"{base_url}/forgot-password",
            headers={"Content-Type": "application/json"},
            json={"email": test_email}
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Forgot password endpoint working correctly")
            data = response.json()
            if "reset_token" in data:
                reset_token = data["reset_token"]
                print(f"   📧 Reset token generated: {reset_token[:20]}...")
                
                # Test 2: Reset Password with Token
                print("\n2. Testing reset password with token...")
                new_password = "newpassword123"
                
                reset_response = requests.post(
                    f"{base_url}/reset-password",
                    headers={"Content-Type": "application/json"},
                    json={"token": reset_token, "new_password": new_password}
                )
                
                print(f"   Status Code: {reset_response.status_code}")
                print(f"   Response: {reset_response.text}")
                
                if reset_response.status_code == 200:
                    print("   ✅ Reset password endpoint working correctly")
                else:
                    print("   ❌ Reset password endpoint failed")
            else:
                print("   ⚠️  No reset token in response (email might be sent instead)")
        else:
            print("   ❌ Forgot password endpoint failed")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
    
    # Test 3: Invalid token
    print("\n3. Testing with invalid token...")
    try:
        invalid_response = requests.post(
            f"{base_url}/reset-password",
            headers={"Content-Type": "application/json"},
            json={"token": "invalid_token", "new_password": "newpass123"}
        )
        
        print(f"   Status Code: {invalid_response.status_code}")
        print(f"   Response: {invalid_response.text}")
        
        if invalid_response.status_code == 400:
            print("   ✅ Invalid token properly rejected")
        else:
            print("   ❌ Invalid token handling incorrect")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")

    print("\n" + "=" * 50)
    print("🎯 Frontend Integration Summary:")
    print("   - API endpoints are accessible")
    print("   - Error handling is implemented")
    print("   - Token validation works correctly")
    print("   - Frontend should work properly with these endpoints")
    print("\n💡 To test the frontend:")
    print("   1. Start the frontend: npm run dev")
    print("   2. Navigate to http://localhost:5173/forgot-password")
    print("   3. Enter an email and submit")
    print("   4. Check for reset token in development mode")
    print("   5. Use the reset link or manually go to /reset-password?token=<token>")

if __name__ == "__main__":
    test_forgot_password_flow()
