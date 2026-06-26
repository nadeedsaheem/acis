import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

import sys
import os
import asyncio
from fastapi.testclient import TestClient


from api.api_server import app
from api import graphrag_service

def test_fallbacks():
    client = TestClient(app)
    
    # 1. Test Neo4j Connection Error Fallback
    print("Testing Neo4j Connection Error Fallback...")
    original_answer_question = graphrag_service.answer_question
    
    def mock_answer_question_connection_err(query):
        raise Exception("ServiceUnavailable: Couldn't connect to localhost:7687")
        
    graphrag_service.answer_question = mock_answer_question_connection_err
    
    res = client.post("/query", json={"repository": "ACIS", "query": "What is SPAposition?"})
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}\n")
    
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "error"
    assert "database is temporarily offline" in data["answer"]
    assert data["sources"] == []
    
    # 2. Test Timeout Error Fallback
    print("Testing Timeout Error Fallback...")
    
    def mock_answer_question_timeout(query):
        # We raise asyncio.TimeoutError inside the thread/async block
        raise asyncio.TimeoutError("Timeout exceeded")
        
    graphrag_service.answer_question = mock_answer_question_timeout
    
    res = client.post("/query", json={"repository": "ACIS", "query": "What is SPAposition?"})
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}\n")
    
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "error"
    assert "request timed out" in data["answer"]
    assert data["sources"] == []

    # 3. Test General Error Fallback
    print("Testing General Error Fallback...")
    
    def mock_answer_question_general(query):
        raise Exception("Some general unexpected API failure")
        
    graphrag_service.answer_question = mock_answer_question_general
    
    res = client.post("/query", json={"repository": "ACIS", "query": "What is SPAposition?"})
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}\n")
    
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "error"
    assert "unexpected API failure" in data["answer"]
    assert data["sources"] == []
    
    # Restore original function
    graphrag_service.answer_question = original_answer_question
    print("ALL FALLBACK TESTS PASSED!")

if __name__ == "__main__":
    test_fallbacks()
