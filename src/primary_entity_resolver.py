import time
from entity_scoring import score_entity

def resolve_primary_entity(query: str, retrieved_entities: list) -> tuple:
    if not retrieved_entities:
        return None, []
        
    scored_entities = []
    for entity in retrieved_entities:
        score = score_entity(query, entity)
        scored_entities.append((score, entity))
        
    # Sort by exact_match (desc), type_score (desc), doc_score (desc), connectivity (desc)
    scored_entities.sort(key=lambda x: x[0], reverse=True)
    
    primary_entity = scored_entities[0][1]
    supporting_entities = [e[1] for e in scored_entities[1:]]
    
    return primary_entity, supporting_entities
