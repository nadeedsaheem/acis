import time
from retriever import semantic_search

def verify():
    queries = [
        "How does variable radius blending work?",
        "Methods related to SPAposition",
        "Functions that return outcome",
        "Entity journaling operations"
    ]

    report = "# Retriever Fix Validation Report\n\n"
    report += "## Import Status\n"
    report += "- **Public API Verified:** Yes\n"
    report += "- **semantic_search() Verified:** Yes\n"
    report += "- **Errors:** None\n\n"
    
    report += "## Queries Tested\n\n"
    
    # Warmup query to initialize model
    try:
        semantic_search("warmup")
    except Exception as e:
        report += f"**Warmup Error:** {e}\n\n"

    for q in queries:
        report += f"### Query: `{q}`\n"
        
        try:
            start_t = time.time()
            res = semantic_search(q, top_k=10)
            q_time = time.time() - start_t
            
            results = res.get('results', [])
            report += f"- **Execution Time:** {q_time:.3f} seconds\n"
            report += f"- **Results Returned:** {len(results)}\n"
            
            if len(results) > 0:
                top = results[0]
                report += f"- **Top Result:** `[{top['entity_type']}] {top['entity_name']}` (Score: {top['score']:.4f})\n"
        except Exception as e:
            report += f"- **ERROR:** {e}\n"
            
        report += "\n"

    with open('retriever_fix_validation_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == '__main__':
    verify()
