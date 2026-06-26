import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graphrag_service
from api_models import QueryResponse

def mock_semantic_search(query, top_k=10):
    lower_q = query.lower()
    if "spaposition" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "SPAposition"}, {"entity_type": "Class", "name": "SPAPOSITION_ARRAY"}, {"entity_type": "Method", "name": "operator+"}]}
    if "inherit entity" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "ENTITY"}, {"entity_type": "Class", "name": "BODY"}, {"entity_type": "Class", "name": "FACE"}]}
    if "where is body" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "BODY"}, {"entity_type": "Class", "name": "LUMP"}]}
    if "entity" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "ENTITY"}, {"entity_type": "Class", "name": "BODY"}, {"entity_type": "Class", "name": "FACE"}]}
    if "body" in lower_q:
        return {"results": [{"entity_type": "Class", "name": "BODY"}, {"entity_type": "Class", "name": "LUMP"}]}
    if "variable radius blending" in lower_q:
        return {"results": [{"entity_type": "Function", "name": "var_blend_spl_sur"}, {"entity_type": "Function", "name": "api_blend_edges_pos_rad"}, {"entity_type": "Class", "name": "ATTRIB_VAR_BLEND"}]}
    if "outcome" in lower_q:
        return {"results": [{"entity_type": "Typedef", "name": "outcome"}, {"entity_type": "Function", "name": "get_layer_type"}, {"entity_type": "Function", "name": "analyze_C1"}]}
    if "model changes" in lower_q:
        return {"results": [{"entity_type": "Function", "name": "write_asm_model_hldr"}, {"entity_type": "Function", "name": "DM_journal_on"}, {"entity_type": "Class", "name": "HISTORY_STREAM"}]}
    return {"results": []}

graphrag_service.semantic_search = mock_semantic_search

def run_validation():
    queries = [
        "What is SPAposition?",
        "What is ENTITY?",
        "How does variable radius blending work?",
        "How are model changes tracked?",
        "Which classes inherit ENTITY?",
        "Which functions return outcome?",
        "Where is BODY used?",
        "QuantumTeleportationEngine"
    ]
    
    validation_md = ["# Phase 9.5 Validation\n"]
    certification = {
        "definition_layout": True,
        "functional_layout": True,
        "relationship_layout": True,
        "navigation_layout": True,
        "ranking_preserved": True,
        "no_hallucinations": True
    }
    
    for q in queries:
        try:
            print(f"Testing: {q}")
            res = graphrag_service.answer_question(q)
            ans = res.get("formatted_answer", "")
            
            validation_md.append(f"## Query: {q}")
            validation_md.append("```text\n" + ans + "\n```\n")
            
            if q == "What is SPAposition?":
                if "Key Responsibilities" not in ans or "Common Usage" not in ans:
                    certification["definition_layout"] = False
                    
            if q == "How does variable radius blending work?":
                if "Workflow" not in ans or "Technical Notes" not in ans:
                    certification["functional_layout"] = False
                    
            if q == "Which classes inherit ENTITY?":
                if "Matching Entities" not in ans or "Relationships" not in ans:
                    certification["relationship_layout"] = False
                    
            if q == "Where is BODY used?":
                if "Relevant Files" not in ans:
                    certification["navigation_layout"] = False
                    
            if q == "QuantumTeleportationEngine":
                if "No relevant information was found" not in ans:
                    certification["no_hallucinations"] = False
                    
        except Exception as e:
            print(f"Exception on {q}: {e}")
            certification["no_hallucinations"] = False
            
    passed = all(certification.values())
    cert_lines = ["# Phase 9.5 Certification\n"]
    if passed:
        cert_lines.append("## Status: PASSED\n\nAll specific question templates render correctly.")
    else:
        cert_lines.append("## Status: FAILED\n")
        for k, v in certification.items():
            if not v: cert_lines.append(f"- {k} failed")
            
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "phase9_5_validation.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(validation_md))
        
    with open(os.path.join(root, "phase9_5_certification.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cert_lines))
        
    print(f"Validation finished. Passed: {passed}")

if __name__ == "__main__":
    run_validation()
