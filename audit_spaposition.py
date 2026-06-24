import json
from retriever import semantic_search
from context_builder import build_context

def run_audit():
    query = "What is SPAposition?"
    
    # 1. Semantic Search
    retrieval_res = semantic_search(query, top_k=10)
    results = retrieval_res.get('results', [])
    
    report = "# SPAposition Retrieval and Prompt Audit\n\n"
    report += f"**Query:** `{query}`\n\n"
    
    report += "## 1. Top 10 Retrieved Nodes & Scores\n\n"
    for i, res in enumerate(results):
        score = res.get('score', 0)
        entity = res.get('entity', {})
        label = entity.get('label', 'Unknown')
        name = entity.get('name', 'Unknown')
        
        doc = res.get('documentation', '')
        if isinstance(doc, dict):
            doc_text = doc.get('text', 'No Text')
        else:
            doc_text = doc
            
        report += f"### {i+1}. {label}: {name} (Score: {score:.4f})\n"
        report += f"**Documentation:**\n```text\n{doc_text}\n```\n"
        report += "\n---\n"
        
    # 2. Expanded Graph Context
    report += "## 2. Expanded Graph Context\n\n"
    context = build_context(results)
    report += "```markdown\n"
    report += context
    report += "\n```\n\n"
    
    # 3. Final Prompt
    report += "## 3. Final Prompt Analysis\n\n"
    system_prompt = "You are an ACIS Knowledge Graph Assistant.\nAnswer only from the supplied graph context."
    user_prompt = f"[GRAPH CONTEXT]\n\n{context}\n\n[QUESTION]\n\n{query}\n\n[INSTRUCTIONS]\n\nAnswer strictly using the graph context."
    
    prompt_size = len(system_prompt) + len(user_prompt)
    report += f"- **Final Prompt Size:** {prompt_size} characters\n\n"
    
    report += "### User Prompt Snippet:\n"
    report += "```text\n"
    report += user_prompt[:1500] + "\n...[truncated]...\n" if len(user_prompt) > 1500 else user_prompt
    report += "\n```\n\n"
    
    # 4. Conclusion
    report += "## 4. Diagnosis and Recommendations\n\n"
    
    has_spaposition = "SPAposition" in context
    
    report += "### Findings:\n"
    if not results:
        report += "A. **Retrieval Issue:** No nodes were retrieved. Vector index or embedding may have failed.\n"
    elif not has_spaposition:
        report += "B. **Context Builder Issue:** The context builder discarded critical information, or retrieval missed the actual `SPAposition` class.\n"
    else:
        report += "C. **Prompt/LLM Issue:** The context contains `SPAposition`, but the LLM provider rejected it. (Note: The fallback mock returns 'Insufficient information' strictly if the exact prompt string doesn't match the hardcoded cases. The real Gemini model might require more explicit class definitions rather than just usages).\n"
        
    report += "\n### Recommendations:\n"
    report += "1. **Embedding Target Expansion:** Currently, only `(:Documentation)` nodes are embedded. `SPAposition` might be a class or struct without a dedicated documentation block, or its documentation is too short. We should embed `Class`, `Struct`, and `Function` signatures alongside their documentation.\n"
    report += "2. **Exact Match Fallback (Hybrid Search):** Implement Hybrid Search. If a query asks 'What is X?', perform an exact match graph lookup for `(:Class {name: 'X'})` and force it into the context before vector retrieval.\n"
    report += "3. **Mock Provider Adjustment:** The current `llm_provider.py` mock strictly matches query strings to bypass rate limits. It returned 'Insufficient information' for this exact string because it was not in the hardcoded whitelist.\n"

    with open('spaposition_audit_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print("Audit generated.")

if __name__ == '__main__':
    run_audit()
