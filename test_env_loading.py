#!/usr/bin/env python3
"""
Test script to verify environment variable loading
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    """Test loading environment variables"""
    
    # Test loading from chatbot_rag-main directory
    env_path = Path(__file__).parent / "chatbot_rag-main" / ".env"
    print(f"Looking for .env file at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print("\nEnvironment variables loaded:")
        print(f"GMAIL_EMAIL: {os.getenv('GMAIL_EMAIL')}")
        print(f"GMAIL_APP_PASSWORD: {os.getenv('GMAIL_APP_PASSWORD')[:10]}..." if os.getenv('GMAIL_APP_PASSWORD') else "GMAIL_APP_PASSWORD: None")
        print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
        print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
        print(f"FRONTEND_URL: {os.getenv('FRONTEND_URL')}")
    else:
        print("ERROR: .env file not found!")

if __name__ == "__main__":
    test_env_loading()
