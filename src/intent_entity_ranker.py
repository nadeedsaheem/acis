def detect_intent(query: str) -> str:
    lower_q = query.lower()
    if "where" in lower_q or "file" in lower_q:
        return "Navigation"
    elif "which" in lower_q or "inherit" in lower_q or "belong" in lower_q or "return" in lower_q:
        return "Relationship"
    elif "how" in lower_q or "work" in lower_q or "operate" in lower_q or "track" in lower_q:
        return "Functional Explanation"
    else:
        return "Definition"

def get_type_score(entity_type: str, intent: str, item: dict = None) -> int:
    # Lower score is better
    if intent == "Definition":
        priorities = {"Class": 1, "Struct": 2, "Enum": 3, "Typedef": 4, "Function": 5, "Method": 6}
        return priorities.get(entity_type, 99)
    elif intent == "Functional Explanation":
        priorities = {"Function": 1, "Method": 2, "Class": 3}
        return priorities.get(entity_type, 99)
    elif intent == "Navigation":
        priorities = {"File": 1, "Class": 2, "Function": 3, "Documentation": 4}
        return priorities.get(entity_type, 99)
    elif intent == "Relationship":
        # Prioritize edges by checking if item has relationship data
        if item:
            if item.get("parent_class"): return 1 # INHERITS/HAS_METHOD
            if item.get("return_type") and item.get("return_type") != "void": return 2 # RETURNS
            if item.get("parameters"): return 3 # HAS_PARAMETER
        return 99
    return 99

def rank_results(query: str, results: list) -> list:
    intent = detect_intent(query)
    
    # Extract core entity word for lexical matching
    words = query.replace("?", "").replace("!", "").split()
    target_words = [w.lower() for w in words if w.lower() not in ["what", "is", "how", "does", "where", "which", "are", "work", "used", "the", "a", "an"]]
    
    def score_result(item):
        entity_type = item.get("entity_type", "Entity")
        name = item.get("name") or item.get("entity_name") or ""
        
        # 1. Exact match gets highest priority
        exact_match = 2
        name_lower = name.lower()
        if any(t == name_lower for t in target_words):
            exact_match = 0 # Exact full string match
        elif any(t in name_lower for t in target_words):
            exact_match = 1 # Substring match
        
        # 2. Type priority based on intent
        type_score = get_type_score(entity_type, intent, item)
        
        return (exact_match, type_score)
        
    return sorted(results, key=score_result)
