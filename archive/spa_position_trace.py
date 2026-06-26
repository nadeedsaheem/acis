import sys
import os

sys.path.insert(0, os.path.abspath('src'))

from query_normalizer import normalize_query
from retriever import semantic_search
from context_builder import build_context
from graphrag_service import answer_question
from llm_provider import LLMProvider

def run_trace():
    query = "What is SPAposition?"
    print("--- TRACE START ---")
    print(f"Original Query: {query}")
    
    normalized = normalize_query(query)
    print(f"Normalized Query: {normalized}")
    
    retrieval_res = semantic_search(normalized, top_k=10)
    results = retrieval_res.get('results', [])
    print(f"Retrieved {len(results)} entities")
    for r in results:
        print(f"  - {r.get('entity_type')}: {r.get('name')}")
        
    context = build_context(results)
    print(f"Context length: {len(context)}")
    
    llm = LLMProvider()
    print(f"LLM Provider: {llm.provider}")
    
    system_prompt = """You are an ACIS Knowledge Graph Assistant.

Answer only from the supplied graph context.

If the answer cannot be determined from the provided context, respond EXACTLY with:
"No relevant information was found in the current knowledge graph.

Try:
• checking the symbol spelling
• asking a broader question
• querying a related class or function"

Do not invent APIs.
Do not invent classes.
Do not invent methods.
Do not assume behavior not present in the context.
Do not use internal phrases like "According to the graph context" or "The graph indicates".
Structure your answers naturally using headings like Definition, Purpose, Typical Usage, and Related Components where applicable.
"""

    user_prompt = f"""[GRAPH CONTEXT]

{context}

[QUESTION]

{normalized}

[INSTRUCTIONS]

Answer strictly using the graph context.
Cite relevant entities when possible.
If insufficient information exists, explicitly output the exact failure message specified in the system prompt.
"""
    
    print("\n--- LLM User Prompt ---")
    print(user_prompt)
    
    answer = llm.generate(system_prompt, user_prompt)
    print("\n--- Raw LLM Answer ---")
    print(answer)
    
    # Run full service
    res = answer_question(query)
    print("\n--- Full Service Answer ---")
    print(res["answer"])
    print("\n--- Formatted Answer ---")
    print(res.get("formatted_answer", ""))

if __name__ == "__main__":
    run_trace()
