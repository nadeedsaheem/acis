import time
from retriever import semantic_search
from context_builder import build_context
from llm_provider import LLMProvider

class GraphRAGService:
    def __init__(self):
        self.llm = LLMProvider()

    def answer_question(self, query: str) -> dict:
        t0 = time.time()
        
        # 1. Retrieval Layer
        retrieval_res = semantic_search(query, top_k=10)
        t1 = time.time()
        retrieval_time = t1 - t0
        
        results = retrieval_res.get('results', [])
        
        # Track Sources
        sources = []
        for r in results:
            sources.append({
                "entity_type": r.get('entity_type', 'Entity'),
                "entity_name": r.get('name') or r.get('entity_name') or 'Unknown'
            })
            
        if not results:
            # 0 results
            return {
                "query": query,
                "answer": "No relevant information found in the knowledge graph.",
                "sources": [],
                "retrieval_time": retrieval_time,
                "generation_time": 0.0,
                "total_time": retrieval_time
            }
            
        # 2. Context Builder
        context = build_context(results)
        
        # 3. LLM Abstraction & Prompting
        system_prompt = """You are an ACIS Knowledge Graph Assistant.

Answer only from the supplied graph context.

If the answer cannot be determined from the provided context, respond:
"Insufficient information found in the knowledge graph."

Do not invent APIs.
Do not invent classes.
Do not invent methods.
Do not assume behavior not present in the context.
"""

        user_prompt = f"""[GRAPH CONTEXT]

{context}

[QUESTION]

{query}

[INSTRUCTIONS]

Answer strictly using the graph context.
Cite relevant entities when possible.
If insufficient information exists, explicitly say so.
"""
        
        # Generate Grounded Answer
        t2 = time.time()
        answer = self.llm.generate(system_prompt, user_prompt)
        t3 = time.time()
        generation_time = t3 - t2
        
        total_time = t3 - t0
        
        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": total_time
        }

# Expose Public API
_service_instance = None

def answer_question(query: str) -> dict:
    global _service_instance
    if _service_instance is None:
        _service_instance = GraphRAGService()
    return _service_instance.answer_question(query)
