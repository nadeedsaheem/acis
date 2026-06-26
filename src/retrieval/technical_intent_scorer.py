import re

EXACT_TERMS = {
    "BODY": 100.0,
    "ENTITY": 100.0,
    "SPAposition": 100.0,
    "journaling": 100.0,
    "outcome": 100.0,
    "spaposition_array": 100.0,
    "history_stream": 100.0,
    "acisjournal": 100.0,
    "attrib_var_blend": 100.0,
    "make_vertex": 100.0,
    "api_initialize_faceter": 100.0
}

WORKFLOW_TERMS = {
    "class": 70.0,
    "method": 70.0,
    "function": 70.0,
    "inherit": 70.0,
    "inherits": 70.0,
    "return": 70.0,
    "parameter": 70.0,
    "call": 70.0,
    "workflow": 70.0,
    "blend": 70.0,
    "blending": 70.0,
    "template": 70.0,
    "namespace": 70.0,
    "topology": 70.0,
    "vertex": 70.0,
    "edge": 70.0,
    "face": 70.0,
    "lump": 70.0,
    "shell": 70.0
}

def score_technical_intent(query: str, normalized_query: str) -> float:
    """
    Returns a technical intent score from 0 to 100.
    Checks for C++ syntax patterns and codebase keywords.
    """
    score = 0.0
    
    # 1. Syntax checks
    if "::" in query:
        score += 80.0
    if "()" in query:
        score += 80.0
    if "api_" in query.lower():
        score += 80.0
        
    # Extract words with underscores included
    words = set(re.findall(r'\b[a-zA-Z_0-9]+\b', query))
    words_lower = set(re.findall(r'\b[a-zA-Z_0-9]+\b', query.lower()))
    
    # 2. Exact case entity checks
    for word in words:
        if word in EXACT_TERMS:
            score += EXACT_TERMS[word]
            
    # 3. Case-insensitive exact entity checks and workflow checks
    for word in words_lower:
        for exact_term, val in EXACT_TERMS.items():
            if word == exact_term.lower():
                score += val
                
        if word in WORKFLOW_TERMS:
            score += WORKFLOW_TERMS[word]
            
    return min(score, 100.0)
