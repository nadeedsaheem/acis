import logging

logger = logging.getLogger(__name__)

def reciprocal_rank_fusion(vector_results: list, lexical_results: list, limit=20, k=60) -> list:
    """
    Combines vector search and lexical search results using Reciprocal Rank Fusion (RRF).
    
    Formula:
    RRF Score = 1 / (k + vector_rank) + 1 / (k + lexical_rank)
    
    Where:
    - rank is 1-indexed (1, 2, ..., N).
    - If a result is only present in vector retrieval, its lexical rank score is 0.
    - If a result is only present in lexical retrieval, its vector rank score is 0.
    """
    rrf_scores = {}
    entity_map = {}
    
    # 1. Process Vector Results
    for index, item in enumerate(vector_results):
        entity_id = item.get("entity_id")
        if not entity_id:
            continue
        rank = index + 1
        score = 1.0 / (k + rank)
        
        rrf_scores[entity_id] = rrf_scores.get(entity_id, 0.0) + score
        if entity_id not in entity_map:
            # Store initial details
            entity_map[entity_id] = {
                "entity_id": entity_id,
                "entity_type": item.get("entity_type") or item.get("type"),
                "entity_name": item.get("entity_name") or item.get("name"),
                "fqn": item.get("entity_fqn") or item.get("fqn") or item.get("entity_name") or item.get("name") or "",
                "documentation": item.get("documentation", ""),
                "context": item.get("context", {}),
                "vector_rank": rank,
                "lexical_rank": None,
                "vector_score": score,
                "lexical_score": 0.0
            }
            
    # 2. Process Lexical Results
    for index, item in enumerate(lexical_results):
        entity_id = item.get("entity_id")
        if not entity_id:
            continue
        rank = index + 1
        score = 1.0 / (k + rank)
        
        rrf_scores[entity_id] = rrf_scores.get(entity_id, 0.0) + score
        if entity_id in entity_map:
            entity_map[entity_id]["lexical_rank"] = rank
            entity_map[entity_id]["lexical_score"] = score
        else:
            entity_map[entity_id] = {
                "entity_id": entity_id,
                "entity_type": item.get("entity_type") or item.get("type"),
                "entity_name": item.get("entity_name") or item.get("name"),
                "fqn": item.get("entity_fqn") or item.get("fqn") or item.get("entity_name") or item.get("name") or "",
                "documentation": item.get("documentation", ""),
                "context": item.get("context", {}),
                "vector_rank": None,
                "lexical_rank": rank,
                "vector_score": 0.0,
                "lexical_score": score
            }
            
    # 3. Sort by aggregated RRF score descending
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    
    # 4. Extract top limit candidates and attach their final score
    fused_results = []
    for entity_id in sorted_ids[:limit]:
        item = entity_map[entity_id]
        item["score"] = rrf_scores[entity_id]
        fused_results.append(item)
        
    logger.info(f"RRF Fusion completed: merged {len(vector_results)} vector & {len(lexical_results)} lexical candidates into {len(fused_results)} top results.")
    return fused_results
