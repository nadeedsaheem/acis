import re
import logging
import os
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_entity_lookup_candidate(query: str) -> bool:
    """
    Check if the query is a candidate for entity lookup.
    Characteristics:
    - 1-3 tokens
    - No question mark
    - No interrogative words
    """
    if "?" in query:
        return False
        
    interrogative_words = {"how", "what", "where", "when", "why", "who", "which", "whose", "can", "do", "does", "is", "are", "explain", "describe", "show"}
    
    tokens = query.strip().split()
    if len(tokens) == 0 or len(tokens) > 3:
        return False
        
    first_word = tokens[0].lower()
    if first_word in interrogative_words:
        return False
        
    if any(word.lower() in interrogative_words for word in tokens):
        return False
        
    return True

def exact_entity_lookup(entity_name: str) -> bool:
    """
    Perform a fast exact lookup against retrieved graph entity names.
    Supported labels: Class, Function, Method, Struct, Enum, Typedef
    """
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        with driver.session() as session:
            query = """
            MATCH (n)
            WHERE (n:Class OR n:Function OR n:Method OR n:Struct OR n:Enum OR n:Typedef)
            AND n.name = $name
            RETURN n.name AS name LIMIT 1
            """
            result = session.run(query, name=entity_name)
            if result.single():
                driver.close()
                return True
        driver.close()
    except Exception as e:
        logger.error(f"Neo4j lookup error: {e}")
        
    return False

def extract_entity_name(query: str) -> str:
    """
    Extract the core entity name from a candidate query.
    E.g. 'SPAposition class' -> 'SPAposition'
    """
    tokens = query.strip().split()
    if len(tokens) > 1 and tokens[1].lower() in ['class', 'struct', 'function', 'method', 'enum', 'typedef']:
        return tokens[0]
    return tokens[0]

def normalize_query(query: str) -> str:
    """
    Normalize the query if it's an entity lookup.
    """
    original_query = query
    if is_entity_lookup_candidate(query):
        entity_name = extract_entity_name(query)
        if exact_entity_lookup(entity_name):
            query = f"What is {entity_name}?"
            
    if original_query != query:
        logger.info(f"Original: {original_query}")
        logger.info(f"Normalized: {query}")
        
    return query
