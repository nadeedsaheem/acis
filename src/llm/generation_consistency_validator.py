import re

def validate_generation(answer: str, primary_entity_name: str) -> bool:
    """
    Validates that the generated answer is actually describing the primary_entity_name.
    Extracts the subject of the first sentence and checks if the primary entity is present.
    """
    if not primary_entity_name:
        return True
        
    # Remove markdown headers to get actual text
    lines = [line.strip() for line in answer.split('\n') if line.strip() and not line.startswith('#')]
    if not lines:
        return True
        
    first_text = " ".join(lines[:2])
    first_sentence = first_text.split('.')[0]
    
    # 1. Simple existence check: the primary entity MUST be in the first 200 chars.
    if primary_entity_name.lower() not in first_text[:200].lower():
        return False
        
    # 2. Subject validation heuristic:
    # Most definitions follow "X is...", "The X class represents...", "X provides..."
    # Find the first occurrence of these verb phrases.
    match = re.search(r'\b(is|represents|defines|provides|acts as|contains|serves as|manages)\b', first_sentence, re.IGNORECASE)
    if match:
        subject_part = first_sentence[:match.start()]
        # If the primary entity is not in the subject part, it likely hijacked to a parent class
        if primary_entity_name.lower() not in subject_part.lower():
            return False
            
    return True
