#!/usr/bin/env python3
"""
Test script to verify the database parameter binding fix
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'chatbot_rag-main'))

from database.db_service import ChatService
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_chat_message_insertion():
    """Test adding chat messages to verify the parameter binding fix"""
    try:
        # Initialize chat service
        chat_service = ChatService()
        
        # Create a test session
        session_id = str(uuid.uuid4())
        user_id = 1  # Assuming we have a user with ID 1
        
        # Create chat session
        chat_service.create_chat_session(session_id, user_id)
        
        # Test adding a user message
        user_message = chat_service.add_chat_message(
            session_id, 
            "user", 
            "Hello, I'd like to order a coffee"
        )
        print(f"✅ User message added successfully: {user_message}")
        
        # Test adding an assistant message with intent and agent
        assistant_message = chat_service.add_chat_message(
            session_id,
            "assistant", 
            "Great! I'd be happy to help you order a coffee. What type would you like?",
            "sales",
            "Product Specialist"
        )
        print(f"✅ Assistant message added successfully: {assistant_message}")
        
        # Test with None values
        none_message = chat_service.add_chat_message(
            session_id,
            "assistant",
            "Another response",
            None,
            None
        )
        print(f"✅ Message with None values added successfully: {none_message}")
        
        # Get chat history to verify
        history = chat_service.get_chat_history(session_id)
        print(f"✅ Chat history retrieved: {len(history)} messages")
        
        for msg in history:
            print(f"  - {msg['role']}: {msg['content'][:50]}... (intent: {msg['intent']}, agent: {msg['agent']})")
        
        print("\n🎉 All tests passed! The database parameter binding issue is fixed.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        try:
            chat_service.close_connection()
        except:
            pass

if __name__ == "__main__":
    success = test_chat_message_insertion()
    sys.exit(0 if success else 1)
