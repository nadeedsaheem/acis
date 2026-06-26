from retrieval.intent_entity_ranker import detect_intent

def score_entity(query: str, item: dict) -> tuple:
    intent = detect_intent(query)
    
    words = query.replace("?", "").replace("!", "").split()
    target_words = [w.lower() for w in words if w.lower() not in ["what", "is", "how", "does", "where", "which", "are", "work", "used", "the", "a", "an"]]
    
    entity_type = item.get("entity_type", "Entity")
    name = item.get("name") or item.get("entity_name") or ""
    name_lower = name.lower()
    
    # 1. Exact Name Match (Lexical Match)
    exact_match = 0
    if any(t == name_lower for t in target_words):
        exact_match = 2
    elif any(t in name_lower for t in target_words):
        exact_match = 1
        
    # 2. Entity Type Priority
    type_score = 0
    if intent == "Definition":
        priorities = {"Class": 6, "Struct": 5, "Enum": 4, "Typedef": 3, "Function": 2, "Method": 1}
        type_score = priorities.get(entity_type, 0)
    elif intent == "Functional Explanation":
        priorities = {"Function": 3, "Method": 2, "Class": 1}
        type_score = priorities.get(entity_type, 0)
    elif intent == "Relationship":
        priorities = {"Class": 3}
        type_score = priorities.get(entity_type, 0)
        if item.get("context") and isinstance(item["context"], dict):
            if item["context"].get("parent_class") or item["context"].get("parents"): 
                type_score += 1
                
    # 3. Documentation Score
    doc_text = item.get("documentation", "")
    doc_score = len(doc_text)
    
    # 4. Graph Connectivity
    connectivity = 0
    context = item.get("context", {})
    if isinstance(context, dict):
        if context.get("methods"): connectivity += len(context["methods"])
        if context.get("parents"): connectivity += len(context["parents"])
        if context.get("parameters"): connectivity += len(context["parameters"])
        if context.get("return_type") and context.get("return_type") != "void": connectivity += 1
        if context.get("parent_class"): connectivity += 1
        
    return (exact_match, type_score, doc_score, connectivity)
