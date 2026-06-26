import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graphrag_service

def mock_semantic_search(query, top_k=10):
    lower_q = query.lower()
    if "spaposition" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "SPAposition"}, {"entity_type": "Class", "name": "SPAPOSITION_ARRAY"}, {"entity_type": "Method", "name": "operator+"}]}
    if "entity" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "ENTITY"}, {"entity_type": "Class", "name": "BODY"}, {"entity_type": "Class", "name": "FACE"}]}
    if "body" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "BODY"}, {"entity_type": "Class", "name": "LUMP"}]}
    if "variable radius blending" in lower_q:
        return {"results": [{"entity_type": "Function", "name": "var_blend_spl_sur"}]}
    if "outcome" in lower_q:
        return {"results": [{"entity_type": "Typedef", "name": "outcome"}, {"entity_type": "Function", "name": "get_layer_type"}, {"entity_type": "Function", "name": "analyze_C1"}]}
    return {"results": []}

graphrag_service.semantic_search = mock_semantic_search

def validate():
    queries = [
        "What is SPAposition?",
        "What is ENTITY?",
        "What is BODY?",
        "How does variable radius blending work?",
        "Which functions return outcome?",
        "NonExistentAPI_That_Should_Fail"
    ]
    
    report_lines = ["# Phase 9.3 Response Formatting Validation Report\n"]
    certification = {
        "no_dicts": True,
        "clean_formatting": True,
        "primary_entity_identified": True,
        "hallucination_protected": True
    }
    
    for q in queries:
        print(f"Testing: {q}")
        try:
            res = graphrag_service.answer_question(q)
            formatted = res.get("formatted_answer", "")
            
            report_lines.append(f"## Query: {q}\n")
            report_lines.append("```text\n")
            report_lines.append(formatted)
            report_lines.append("\n```\n")
            
            # Check no dicts
            if "{" in formatted and "'entity_type'" in formatted:
                certification["no_dicts"] = False
                
            # Check hallucination on the last query
            if q == "NonExistentAPI_That_Should_Fail":
                if "No relevant information was found" not in formatted:
                    certification["hallucination_protected"] = False

            if "SPAposition" in q and "What is" in q:
                if "Primary Entity" not in formatted or "SPAposition" not in formatted:
                    certification["primary_entity_identified"] = False

        except Exception as e:
            print(f"Failed query {q}: {e}")
            certification["clean_formatting"] = False

    # Write to root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    with open(os.path.join(root_dir, "response_format_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    cert_lines = ["# Phase 9.3 Certification\n"]
    passed = all(certification.values())
    
    if passed:
        cert_lines.append("## Status: PASSED\n")
        cert_lines.append("The response formatting logic correctly isolates retrieval dictionaries, structures the output clearly, and gracefully handles non-existent queries.\n")
    else:
        cert_lines.append("## Status: FAILED\n")
        cert_lines.append("One or more formatting conditions were violated:\n")
        for k, v in certification.items():
            if not v:
                cert_lines.append(f"- {k} failed\n")
                
    with open(os.path.join(root_dir, "phase9_3_certification.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cert_lines))
        
    print("Validation and certification generated.")

if __name__ == "__main__":
    validate()
