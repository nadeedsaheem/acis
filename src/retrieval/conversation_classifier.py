import re

# Intent Categories
CATEGORY_GREETING = "greeting"
CATEGORY_SMALL_TALK = "small_talk"
CATEGORY_HELP = "help"
CATEGORY_RETRIEVAL = "retrieval"

# Conversational word sets for exact matching
GREETING_WORDS = {"hi", "hello", "hey", "greetings", "yo", "hola", "sup"}
GREETING_PHRASES = {"good morning", "good evening", "good afternoon", "good day"}

SMALL_TALK_WORDS = {
    "thanks", "thank you", "ty", "thx", "goodbye", "bye", "awesome", 
    "cool", "great", "perfect", "ok", "okay", "fine"
}
SMALL_TALK_PHRASES = {
    "how are you", 
    "how are you doing", 
    "who are you", 
    "what are you", 
    "tell me about yourself",
    "how is it going",
    "how's it going",
    "are you a robot",
    "are you an ai"
}

HELP_WORDS = {"help", "examples", "info", "usage"}
HELP_PHRASES = {
    "what can you do",
    "what do you do",
    "how do i use you",
    "how to use",
    "show me examples",
    "show examples"
}

# Codebase keywords that always override conversational matching and force retrieval
CODEBASE_KEYWORDS = {
    "body", "spaposition", "entity", "blend", "blending", "journal", "journaling", 
    "inherit", "inherits", "class", "method", "function", "struct", "enum", 
    "api", "edge", "face", "wire", "lump", "shell", "vertex", "topology", "call", 
    "attribute", "relationship", "parent", "return", "outcome", "spaposition_array",
    "history_stream", "acisjournal", "attrib_var_blend"
}

def clean_query(query: str) -> str:
    """Normalize input query for classification."""
    if not query:
        return ""
    q = query.lower().strip()
    # Remove trailing punctuation (question marks, exclamation points, periods)
    q = re.sub(r'[?!.]+$', '', q)
    # Collapse multiple whitespaces
    q = re.sub(r'\s+', ' ', q)
    return q.strip()

def classify_query(query: str) -> str:
    """
    Classify a query into one of: 'greeting', 'small_talk', 'help', or 'retrieval'.
    Runs entirely via local rule-based sets and regex patterns to guarantee < 1ms latency.
    """
    cleaned = clean_query(query)
    if not cleaned:
        return CATEGORY_RETRIEVAL

    # 1. Overriding Check: If the query contains any codebase keyword or code syntax, force retrieval
    # Code syntax checks: C++ namespace separator (::) or function call signature parens (())
    if "::" in cleaned or "()" in cleaned:
        return CATEGORY_RETRIEVAL
        
    words = set(re.findall(r'\b[a-z_0-9]+\b', cleaned))
    if words & CODEBASE_KEYWORDS:
        return CATEGORY_RETRIEVAL

    # 2. Exact word or phrase matches
    if cleaned in GREETING_WORDS or cleaned in GREETING_PHRASES:
        return CATEGORY_GREETING
        
    if cleaned in SMALL_TALK_WORDS or cleaned in SMALL_TALK_PHRASES:
        return CATEGORY_SMALL_TALK
        
    if cleaned in HELP_WORDS or cleaned in HELP_PHRASES:
        return CATEGORY_HELP

    # 3. Soft regex pattern matches for greeting/small talk/help at start or end of text,
    # as long as they passed the codebase keyword override above.
    if re.match(r'^(hi|hello|hey|good morning|good evening)\b', cleaned):
        return CATEGORY_GREETING
        
    if re.match(r'^(thanks|thank you|how are you|who are you)\b', cleaned):
        return CATEGORY_SMALL_TALK
        
    if re.match(r'^(help|examples|what can you do)\b', cleaned):
        return CATEGORY_HELP

    # Fallback to retrieval
    return CATEGORY_RETRIEVAL
