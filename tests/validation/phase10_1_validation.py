import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

import os
import sys


from api import graphrag_service
from llm.llm_provider import LLMProvider

# Mock semantic search for stable renderer testing
def mock_semantic_search(query, top_k=10):
    lower_q = query.lower()
    if "spaposition" in lower_q:
        return {"results": [{"entity_type": "Class", "entity_id": "", "name": "SPAposition"}]}
    if "inherit entity" in lower_q:
        return {"results": [{"entity_type": "Class", "entity_id": "", "name": "ENTITY"}]}
    if "entity" in lower_q:
        return {"results": [{"entity_type": "Class", "entity_id": "", "name": "ENTITY"}]}
    if "variable radius blending" in lower_q:
        return {"results": [{"entity_type": "Class", "entity_id": "", "name": "ATTRIB_VAR_BLEND"}]}
    if "outcome" in lower_q:
        return {"results": [{"entity_type": "Class", "entity_id": "", "name": "outcome"}]}
    if "body" in lower_q:
        return {"results": [{"entity_type": "Class", "entity_id": "", "name": "BODY"}]}
    return {"results": []}

graphrag_service.semantic_search = mock_semantic_search

# Mock the LLM to just output dummy explanations so we can verify the Renderer logic
def mock_generate(self, system_prompt, user_prompt):
    return "## Definition\nMocked Definition from LLM.\n\n## Purpose\nMocked Purpose from LLM.\n\n## Workflow\nMocked Workflow from LLM."

LLMProvider.generate = mock_generate

def run_validation():
    queries = [
        "What is SPAposition?",
        "What is ENTITY?",
        "Which classes inherit ENTITY?",
        "What returns outcome?",
        "How does variable radius blending work?",
        "Where is BODY used?"
    ]
    
    validation_md = ["# Phase 10.1 Validation\n"]
    certification = {
        "llm_explanation_isolation": True,
        "renderer_relationship_injection": True,
        "renderer_evidence_injection": True,
        "entity_prioritization": True
    }
    
    for q in queries:
        try:
            print(f"Testing: {q}")
            res = graphrag_service.answer_question(q)
            ans = res.get("formatted_answer", "").replace('\r', '')
            
            validation_md.append(f"## Query: {q}")
            validation_md.append("```text\n" + ans + "\n```\n")
            
            # The LLM outputs "Mocked Definition from LLM."
            if "Mocked Definition from LLM." not in ans and "Mocked Workflow from LLM." not in ans:
                certification["llm_explanation_isolation"] = False
                
            # If the query is expected to have relationships, check for them outside the LLM block
            if q == "What is SPAposition?":
                if "Knowledge Graph Relationships" not in ans or "Used As Parameter" not in ans:
                    print("Failed to find renderer-injected relationships for SPAposition")
                    certification["renderer_relationship_injection"] = False
                if "SPAposition (Class)" not in ans:
                    certification["entity_prioritization"] = False
                    
            if q == "What is ENTITY?":
                if "Inherited By" not in ans:
                    print("Failed to find Inherited By for ENTITY")
                    certification["renderer_relationship_injection"] = False
                    
            if "Knowledge Graph Evidence" not in ans:
                certification["renderer_evidence_injection"] = False
                
        except Exception as e:
            print(f"Exception on {q}: {e}")
            certification["renderer_relationship_injection"] = False
            
    passed = all(certification.values())
    cert_lines = ["# Phase 10.1 Certification\n"]
    if passed:
        cert_lines.append("## Status: PASSED\n\nAll strict Graph rendering separation features implemented successfully.")
    else:
        cert_lines.append("## Status: FAILED\n")
        for k, v in certification.items():
            if not v: cert_lines.append(f"- {k} failed")
            
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(root, "phase10_1_validation.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(validation_md))
        
    with open(os.path.join(root, "phase10_1_certification.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cert_lines))
        
    print(f"Validation finished. Passed: {passed}")

if __name__ == "__main__":
    run_validation()
