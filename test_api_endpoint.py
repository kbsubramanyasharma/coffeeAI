#!/usr/bin/env python3
"""
Test the actual API endpoint for forgot password
"""

import requests
import json

def test_forgot_password_api():
    """Test the forgot password API endpoint"""
    try:
        # API endpoint
        url = "http://localhost:8000/api/v1/forgot-password"
        
        # Request data (same format your frontend should use)
        data = {
            "email": "kbsubrhamanyasharma9632@gmail.com"
        }
        
        print("Testing forgot password API endpoint...")
        print(f"URL: {url}")
        print(f"Data: {data}")
        
        # Make the API request
        response = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ API call successful!")
            response_data = response.json()
            print(f"✓ Message: {response_data.get('message', 'No message')}")
            return True
        else:
            print("✗ API call failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - make sure server is running on port 8000")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("Testing Forgot Password API Endpoint")
    print("=" * 50)
    
    success = test_forgot_password_api()
    
    print("=" * 50)
    if success:
        print("✅ API endpoint is working!")
        print("\n📧 Check your email inbox:")
        print("   - kbsubrhamanyasharma9632@gmail.com")
        print("   - Check spam/junk folder")
        print("   - Check promotions tab")
        print("\n🔍 Frontend should call:")
        print("   POST http://localhost:8000/api/v1/forgot-password")
        print("   Body: {\"email\": \"user@example.com\"}")
    else:
        print("❌ API endpoint has issues!")

if __name__ == "__main__":
    main()
