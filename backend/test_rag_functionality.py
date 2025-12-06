# Test script for RAG functionality in the Humanoid Robotics AI-Driven Textbook project

import os
import requests
import json

def test_rag_functionality():
    """
    Test script to validate the RAG functionality locally
    """
    base_url = "http://localhost:8000"
    
    print("Testing RAG functionality...")
    print(f"Base URL: {base_url}")
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✓ Health check passed: {health_data}")
        else:
            print(f"   ✗ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Health check failed with error: {e}")
    
    # Test 2: Get all chapters
    print("\n2. Testing chapters endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/chapters")
        if response.status_code == 200:
            chapters_data = response.json()
            print(f"   ✓ Chapters endpoint passed, found {len(chapters_data.get('chapters', []))} chapters")
        else:
            print(f"   ✗ Chapters endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Chapters endpoint failed with error: {e}")
    
    # Test 3: Query endpoint (if you want to test with a specific query)
    print("\n3. Testing query endpoint...")
    try:
        query_payload = {
            "query": "humanoid robotics",
            "top_k": 3
        }
        response = requests.post(
            f"{base_url}/api/v1/query",
            json=query_payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            query_result = response.json()
            print(f"   ✓ Query endpoint passed, got {len(query_result.get('results', []))} results")
        else:
            print(f"   ✗ Query endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Query endpoint failed with error: {e}")
    
    # Test 4: Chat endpoint (this requires the indexing to be done)
    print("\n4. Testing chat endpoint...")
    try:
        chat_payload = {
            "message": "What are the key components of humanoid robotics?",
            "top_k": 3,
            "temperature": 0.7
        }
        response = requests.post(
            f"{base_url}/api/v1/chat",
            json=chat_payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            chat_result = response.json()
            print(f"   ✓ Chat endpoint passed")
            print(f"   Response preview: {chat_result.get('response', '')[:100]}...")
        else:
            print(f"   ✗ Chat endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Chat endpoint failed with error: {e}")
    
    # Test 5: Check API documentation
    print("\n5. Checking API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("   ✓ API documentation is accessible at /docs")
        else:
            print(f"   ✗ API documentation not accessible, status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Failed to access API documentation: {e}")

def start_instructions():
    """
    Provide instructions for starting the backend service
    """
    print("\n" + "="*60)
    print("TO START THE BACKEND SERVICE:")
    print("="*60)
    print("1. Navigate to the backend directory:")
    print("   cd backend")
    print("")
    print("2. Set up your environment variables:")
    print("   Create a .env file or set GEMINI_API_KEY environment variable")
    print("   GEMINI_API_KEY=your_gemini_api_key_here")
    print("")
    print("3. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("")
    print("4. Start the service:")
    print("   uvicorn api.main:app --reload --port 8000")
    print("")
    print("5. Make sure Qdrant is running (either locally or cloud instance)")
    print("="*60)

if __name__ == "__main__":
    start_instructions()
    print("\nAfter starting the service, run this test script again to validate the RAG functionality.")