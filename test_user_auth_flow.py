#!/usr/bin/env python3
"""
Test script to verify the user authentication flow in the chatbot
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_guest_user_flow():
    """Test chatbot with no user_id (guest user flow)"""
    print("\n=== Testing Guest User Flow ===")
    
    response = requests.post(f"{BASE_URL}/api/chatbot", json={
        "message": "Hello, I want to order a coffee",
        "session_id": "test-guest-session-123"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Guest user response: {data.get('reply', '')[:100]}...")
        print(f"Session ID: {data.get('session_id')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_logged_in_user_flow():
    """Test chatbot with user_id (logged-in user flow)"""
    print("\n=== Testing Logged-in User Flow ===")
    
    # First, register a test user
    register_response = requests.post(f"{BASE_URL}/api/v1/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123"
    })
    
    if register_response.status_code == 200:
        user_data = register_response.json()
        user_id = user_data.get("user_id")
        print(f"✅ User registered with ID: {user_id}")
        
        # Test chatbot with user_id
        response = requests.post(f"{BASE_URL}/api/chatbot", json={
            "message": "Hello, I want to order a coffee",
            "session_id": "test-logged-in-session-456",
            "user_id": user_id
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logged-in user response: {data.get('reply', '')[:100]}...")
            print(f"Session ID: {data.get('session_id')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    else:
        # Try login instead if user already exists
        print("Registration failed, trying login...")
        login_response = requests.post(f"{BASE_URL}/api/v1/login", json={
            "email": "testuser@example.com",
            "password": "testpassword123"
        })
        
        if login_response.status_code == 200:
            user_data = login_response.json()
            user_id = user_data.get("user_id")
            print(f"✅ User logged in with ID: {user_id}")
            
            # Test chatbot with user_id
            response = requests.post(f"{BASE_URL}/api/chatbot", json={
                "message": "Hello, I want to order a coffee",
                "session_id": "test-logged-in-session-456",
                "user_id": user_id
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Logged-in user response: {data.get('reply', '')[:100]}...")
                print(f"Session ID: {data.get('session_id')}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        else:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")

if __name__ == "__main__":
    print("Testing User Authentication Flow in Chatbot")
    print("Make sure the FastAPI server is running on localhost:8000")
    
    try:
        # Test server connectivity
        health_response = requests.get(f"{BASE_URL}/")
        if health_response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server not responding correctly")
            exit(1)
            
        test_guest_user_flow()
        test_logged_in_user_flow()
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
