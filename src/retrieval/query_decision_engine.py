import time
from retrieval.query_normalizer import normalize_query
from retrieval.conversation_confidence import score_conversational_intent
from retrieval.technical_intent_scorer import score_technical_intent
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

AMBIGUOUS_RESPONSE = (
    "I couldn't determine whether this is a conversational message or a code question.\n\n"
    "Examples:\n"
    "- What is BODY?\n"
    "- What is SPAposition?\n"
    "- Which classes inherit ENTITY?\n"
    "- Explain journaling."
)

def get_small_talk_response(query_cleaned: str) -> str:
    if "thank" in query_cleaned:
        return "You're welcome! Let me know if you need help exploring the ACIS codebase."
    if "how are you" in query_cleaned:
        return "I'm doing well, thank you! How can I assist you with the ACIS codebase today?"
    if "who are you" in query_cleaned or "what are you" in query_cleaned:
        return "I am the ACIS GraphRAG Assistant, trained on the structure and documentation of the ACIS geometric modeling kernel."
    return "I am here and ready to help you with the ACIS codebase."

def wrap_static_response(query: str, answer: str, start_time: float) -> dict:
    result = {
        "query": query,
        "answer": answer,
        "sources": [],
        "full_results": [],
        "retrieval_time": 0.0,
        "generation_time": 0.0,
        "total_time": time.time() - start_time
    }
    return compose_response(result)

def route_query_decisions(query: str, retrieval_callback) -> dict:
    """
    Route the query based on fuzzy conversational confidence and technical intent.
    If the query is conversational (Greeting, Small Talk, or Help), return predefined responses directly,
    bypassing all retrieval and generation loops.
    Otherwise, delegate to retrieval_callback.
    """
    t0 = time.time()
    
    normalized = normalize_query(query)
    conv_score, category = score_conversational_intent(normalized)
    tech_score = score_technical_intent(query, normalized)
    word_count = len(normalized.split())
    
    # 1. Technical query override
    if tech_score > 60.0:
        return retrieval_callback(query)
        
    # 2. Conversational match
    if conv_score > 85.0 and tech_score < 40.0:
        if category == "greeting":
            return wrap_static_response(query, GREETING_RESPONSE, t0)
        elif category == "help":
            return wrap_static_response(query, HELP_RESPONSE, t0)
        else: # small_talk
            return wrap_static_response(query, get_small_talk_response(normalized), t0)
            
    # 3. Guardrail for very short non-technical queries
    if word_count < 3 and tech_score < 40.0 and conv_score < 85.0:
        return wrap_static_response(query, AMBIGUOUS_RESPONSE, t0)
        
    # 4. Anything else is ambiguous
    return wrap_static_response(query, AMBIGUOUS_RESPONSE, t0)
