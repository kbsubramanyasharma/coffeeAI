#!/usr/bin/env python3

import sys
from pathlib import Path

# Add parent to path to import services
sys.path.insert(0, str(Path(__file__).parent))

from core.rag import RAGSystem

def test_rag_retrieval():
    """Test what the RAG system retrieves for Civet Cat"""
    rag_system = RAGSystem(llm_provider="gemini")
    
    # Test retrieval for Civet Cat
    query = "most expensive coffee Civet Cat"
    docs = rag_system.retrieve_relevant_documents(query, k=3)
    
    print("=== RAG System Retrieval Test ===")
    print(f"Query: {query}")
    print(f"Retrieved {len(docs)} documents:")
    
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Document {i} ---")
        print(doc[:300] + "..." if len(doc) > 300 else doc)

if __name__ == "__main__":
    test_rag_retrieval()
