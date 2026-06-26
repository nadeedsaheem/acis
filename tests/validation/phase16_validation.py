import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from api.graphrag_service import answer_question
from llm.generation_consistency_validator import validate_generation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    queries = [
        ("What is BODY?", "BODY"),
        ("What is FACE?", "FACE"),
        ("What is EDGE?", "EDGE")
    ]
    
    results = []
    success = True
    
    for q, entity in queries:
        logger.info(f"Executing query: '{q}'")
        res = answer_question(q)
        answer = res.get("answer", "")
        
        lines = [line.strip() for line in answer.split('\n') if line.strip() and not line.startswith('#')]
        first_sentence = lines[0].split('.')[0] if lines else "NO_ANSWER_GENERATED"
        
        is_valid = validate_generation(answer, entity)
        
        if not is_valid:
            logger.error(f"Validation failed for query '{q}'. Subject seems to be hijacked.")
            success = False
            
        if "ENTITY is" in first_sentence and entity != "ENTITY":
            logger.error(f"Hijack detected: 'ENTITY is' found in first sentence for query '{q}'.")
            success = False
            
        results.append({
            "query": q,
            "expected_entity": entity,
            "first_sentence": first_sentence,
            "is_valid": is_valid
        })
        
    return success, results

def main():
    logger.info("Starting Phase 16 Validation...")
    success, results = run_tests()
    
    report = "# Phase 16 Grounding Enforcement Report\n\n"
    report += "This report verifies that the Primary Entity Grounding Lock successfully prevents the LLM from hijacking the definition section with parent classes (e.g., ENTITY).\n\n"
    
    report += "## 📊 Verification Results\n\n"
    report += "| Query | Expected Entity | Extracted First Sentence | Validated? |\n"
    report += "| :--- | :---: | :--- | :---: |\n"
    
    for r in results:
        report += f"| `{r['query']}` | **{r['expected_entity']}** | {r['first_sentence']} | {'**PASSED**' if r['is_valid'] else 'FAILED'} |\n"
        
    report += f"\n### Overall Status: **{'PASSED' if success else 'FAILED'}**\n"
    
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/reports/grounding_enforcement_report.md'))
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    logger.info(f"Generated benchmark report at {report_path}")
    
    # Copy to artifacts dir
    artifacts_dir = "C:\\Users\\Dell\\.gemini\\antigravity\\brain\\f4be7305-887d-4ced-85b7-7e8d9e569b25"
    if os.path.exists(artifacts_dir):
        with open(os.path.join(artifacts_dir, 'grounding_enforcement_report.md'), 'w', encoding='utf-8') as f:
            f.write(report)
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
