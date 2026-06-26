import time
from retrieval.retriever import semantic_search
from llm.context_builder import build_context
from llm.llm_provider import LLMProvider
from retrieval.intent_entity_ranker import rank_results
from retrieval.primary_entity_resolver import resolve_primary_entity
from llm.grounded_answer_synthesizer import build_synthesis_prompt
from llm.response_composer import compose_response
from graph.graph_context_enricher import enrich_context

class GraphRAGService:
    def __init__(self):
        self.llm = LLMProvider()

    def answer_question(self, query: str) -> dict:
        t0 = time.time()
        
        # 1. Retrieval Layer
        retrieval_res = semantic_search(query, top_k=20)
        t1 = time.time()
        retrieval_time = t1 - t0
        
        results = retrieval_res.get('results', [])
        
        # 1.5 Intent-Aware Ranking
        if results:
            results = rank_results(query, results)
        
        # 1.6 Primary Entity Resolution
        primary_entity, supporting_entities = resolve_primary_entity(query, results) if results else (None, [])
        
        # Track Sources
        sources = []
        if primary_entity:
            sources.append({
                "entity_type": primary_entity.get('entity_type', 'Entity'),
                "entity_name": primary_entity.get('name') or primary_entity.get('entity_name') or 'Unknown',
                "is_primary": True
            })
        for r in supporting_entities:
            sources.append({
                "entity_type": r.get('entity_type', 'Entity'),
                "entity_name": r.get('name') or r.get('entity_name') or 'Unknown',
                "is_primary": False
            })
            
        if not results:
            # 0 results
            empty_res = {
                "query": query,
                "answer": "No relevant information was found in the current knowledge graph.\n\nSuggestions\n\n• Verify the symbol spelling.\n• Ask about a related class or function.\n• Use a broader technical description.",
                "sources": [],
                "full_results": [],
                "retrieval_time": retrieval_time,
                "generation_time": 0.0,
                "total_time": retrieval_time
            }
            empty_res = compose_response(empty_res)
            return empty_res
            
        # 1.8 Graph Context Enrichment
        enriched_primary = enrich_context([primary_entity], query) if primary_entity else []
        
        # 2. Context Builder
        context = build_context(enriched_primary, supporting_entities)
        
        # Merge back full results for response composer
        enriched_results = enriched_primary + supporting_entities
        
        # 3. LLM Abstraction & Prompting
        primary_entity_name = primary_entity.get('name') or primary_entity.get('entity_name') if primary_entity else None
        
        system_prompt, user_prompt, category = build_synthesis_prompt(query, context, primary_entity_name=primary_entity_name, is_retry=False)
        
        # Generate Grounded Answer
        t2 = time.time()
        answer = self.llm.generate(system_prompt, user_prompt)
        
        from llm.generation_consistency_validator import validate_generation
        if not validate_generation(answer, primary_entity_name):
            import logging
            logging.warning(f"Generation hijacked! Regenerating response for {primary_entity_name}...")
            system_prompt, user_prompt, category = build_synthesis_prompt(query, context, primary_entity_name=primary_entity_name, is_retry=True)
            answer = self.llm.generate(system_prompt, user_prompt)
            
        t3 = time.time()
        generation_time = t3 - t2
        
        total_time = t3 - t0
        
        result_dict = {
            "query": query,
            "answer": answer,
            "sources": sources,
            "full_results": enriched_results,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": total_time
        }
        
        return compose_response(result_dict)

# Expose Public API
_service_instance = None

def answer_question(query: str) -> dict:
    global _service_instance
    if _service_instance is None:
        _service_instance = GraphRAGService()
    from retrieval.query_decision_engine import route_query_decisions
    return route_query_decisions(query, _service_instance.answer_question)
