import time
from retrieval.conversation_classifier import (
    classify_query, 
    clean_query, 
    CATEGORY_GREETING, 
    CATEGORY_SMALL_TALK, 
    CATEGORY_HELP
)
from llm.response_composer import compose_response

# Predefined response blocks matching requirements
GREETING_RESPONSE = (
    "Hello! I am the ACIS GraphRAG Assistant.\n\n"
    "I can answer questions about:\n\n"
    "• Classes\n"
    "• Methods\n"
    "• Inheritance\n"
    "• Call Graphs\n"
    "• Parameters\n"
    "• Return Types\n"
    "• Modeling Workflows\n\n"
    "Example Questions:\n"
    "- What is BODY?\n"
    "- What is SPAposition?\n"
    "- Which classes inherit ENTITY?\n"
    "- How does variable radius blending work?"
)

HELP_RESPONSE = (
    "I am the ACIS GraphRAG Assistant, designed to help you navigate and query the ACIS geometric modeling kernel.\n\n"
    "You can ask me questions like:\n"
    "• \"What is BODY?\" (class definitions & attributes)\n"
    "• \"What is SPAposition?\" (struct definitions & components)\n"
    "• \"Which classes inherit ENTITY?\" (inheritance & hierarchy)\n"
    "• \"How does variable radius blending work?\" (modeling workflow details)\n"
    "• \"How are topology changes tracked?\" (procedural call tree exploration)"
)

def get_small_talk_response(query_cleaned: str) -> str:
    """Provide specific conversational response based on small talk keywords."""
    if "thank" in query_cleaned:
        return "You're welcome! Let me know if you need help exploring the ACIS codebase."
    if "how are you" in query_cleaned:
        return "I'm doing well, thank you! How can I assist you with the ACIS codebase today?"
    if "who are you" in query_cleaned or "what are you" in query_cleaned:
        return "I am the ACIS GraphRAG Assistant, trained on the structure and documentation of the ACIS geometric modeling kernel."
    return "I am here and ready to help you with the ACIS codebase."

def route_query(query: str, retrieval_callback) -> dict:
    """
    Route the query based on classification.
    If the query is conversational (Greeting, Small Talk, or Help), return predefined responses directly,
    bypassing all retrieval and generation loops.
    Otherwise, delegate to retrieval_callback.
    """
    t0 = time.time()
    category = classify_query(query)
    
    if category == CATEGORY_GREETING:
        result = {
            "query": query,
            "answer": GREETING_RESPONSE,
            "sources": [],
            "full_results": [],
            "retrieval_time": 0.0,
            "generation_time": 0.0,
            "total_time": time.time() - t0
        }
        return compose_response(result)
        
    elif category == CATEGORY_HELP:
        result = {
            "query": query,
            "answer": HELP_RESPONSE,
            "sources": [],
            "full_results": [],
            "retrieval_time": 0.0,
            "generation_time": 0.0,
            "total_time": time.time() - t0
        }
        return compose_response(result)
        
    elif category == CATEGORY_SMALL_TALK:
        cleaned = clean_query(query)
        result = {
            "query": query,
            "answer": get_small_talk_response(cleaned),
            "sources": [],
            "full_results": [],
            "retrieval_time": 0.0,
            "generation_time": 0.0,
            "total_time": time.time() - t0
        }
        return compose_response(result)
        
    # Otherwise, trigger retrieval and LLM pipeline
    return retrieval_callback(query)
