import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

import time
from api.graphrag_service import answer_question
from llm.llm_provider import LLMProvider

def run_real_llm_validation():
    llm_instance = LLMProvider()
    model_used = llm_instance.provider
    if model_used == "gemini":
        model_name = "gemini-2.5-flash"
    else:
        model_name = model_used

    standard_queries = [
        "How does variable radius blending work?",
        "Which functions return outcome?",
        "Methods related to SPAposition?",
        "How does journaling operate?",
        "Which classes inherit ENTITY?"
    ]

    hallucination_queries = [
        "How does the ACIS quantum teleportation engine work?",
        "Explain the lunar navigation subsystem in ACIS."
    ]

    report = "# Phase 8.1 Real LLM Validation Report\n\n"
    report += f"- **Model Used:** `{model_name}`\n\n"
    
    total_time_sum = 0
    total_queries = 0
    
    # No warmup to save API quota


    report += "## Standard Queries\n\n"
    for q in standard_queries:
        report += f"### Query: `{q}`\n"
        
        try:
            res = answer_question(q)
            
            total_time_sum += res['total_time']
            total_queries += 1
            
            from retrieval.retriever import semantic_search
            from context_builder import build_context
            retrieval_res = semantic_search(q, top_k=10)
            context = build_context(retrieval_res.get('results', []))
            prompt_size = len(context)

            report += f"- **Retrieval Sources:** {len(res['sources'])}\n"
            report += f"- **Prompt Size:** ~{prompt_size} characters\n"
            report += f"- **Retrieval Time:** {res['retrieval_time']:.3f}s\n"
            report += f"- **Generation Time:** {res['generation_time']:.3f}s\n"
            report += f"- **Total Time:** {res['total_time']:.3f}s\n"
            report += f"- **Answer:** {res['answer']}\n\n"
            
        except Exception as e:
            report += f"- **ERROR:** {e}\n\n"

    report += "## Hallucination Tests\n\n"
    for q in hallucination_queries:
        report += f"### Query: `{q}`\n"
        
        try:
            res = answer_question(q)
            
            total_time_sum += res['total_time']
            total_queries += 1
            
            from retrieval.retriever import semantic_search
            from context_builder import build_context
            retrieval_res = semantic_search(q, top_k=10)
            context = build_context(retrieval_res.get('results', []))
            prompt_size = len(context)

            report += f"- **Retrieval Sources:** {len(res['sources'])}\n"
            report += f"- **Prompt Size:** ~{prompt_size} characters\n"
            report += f"- **Total Time:** {res['total_time']:.3f}s\n"
            report += f"- **Answer:** {res['answer']}\n\n"
            
        except Exception as e:
            report += f"- **ERROR:** {e}\n\n"

    avg_time = total_time_sum / total_queries if total_queries > 0 else 0
    report += f"## Summary\n"
    report += f"- **Average Response Time:** {avg_time:.3f}s\n"

    with open('real_llm_validation_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == '__main__':
    run_real_llm_validation()
