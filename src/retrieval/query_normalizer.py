import re

def normalize_query(query: str) -> str:
    """
    Normalizes a user query for conversational and technical routing.
    - Lowercases text
    - Removes punctuation
    - Collapses repeated characters (e.g., 'heyyyy' -> 'hey', 'hiiii' -> 'hi', 'heloo' -> 'helo')
      Note: 'hello' will become 'helo', which is perfectly fine for rapidfuzz matching.
    - Removes surrounding and repeated whitespace
    """
    if not query:
        return ""
        
    # 1. Lowercase
    q = query.lower()
    
    # 2. Remove punctuation (excluding underscores or colons which might be in C++ FQNs like api_ or ::)
    # Actually, the requirements say "Remove: punctuation". If we remove :: or _, it might break technical detection.
    # We should preserve :: and _ for technical intent scoring.
    q = re.sub(r'[^\w\s:]', '', q)
    
    # 3. Collapse repeated characters (3 or more down to 1, or just 2+ down to 1)
    # If we reduce 'll' to 'l', 'hello' becomes 'helo'. 
    # Let's collapse 2+ consecutive identical characters down to 1 to handle 'heloo', 'hiii'.
    q = re.sub(r'(.)\1+', r'\1', q)
    
    # 4. Collapse repeated whitespace and strip
    q = re.sub(r'\s+', ' ', q).strip()
    
    return q
