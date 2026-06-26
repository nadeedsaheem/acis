import os
import sys
import logging
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from retrieval.query_decision_engine import route_query_decisions
from retrieval.query_normalizer import normalize_query
from retrieval.conversation_confidence import score_conversational_intent
from retrieval.technical_intent_scorer import score_technical_intent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_routing():
    queries = {
        "hi": False,
        "hello": False,
        "heloo": False,
        "hii": False,
        "thnks": False,
        "ok": False,
        "hello what is BODY": True,
        "explain journaling": True,
        "SPAposition": True
    }
    
    results = []
    failed = False
    
    for q, expected_retrieval in queries.items():
        retrieval_called = False
        def dummy_retrieval(query):
            nonlocal retrieval_called
            retrieval_called = True
            return {"answer": "Retrieval result"}
            
        # Get intermediate scores for report
        n_q = normalize_query(q)
        conv_score, cat = score_conversational_intent(n_q)
        tech_score = score_technical_intent(q, n_q)
        
        response = route_query_decisions(q, dummy_retrieval)
        
        # Verify
        passed = (retrieval_called == expected_retrieval)
        if not passed:
            failed = True
            logger.error(f"Routing failed for '{q}'. Expected retrieval={expected_retrieval}, got {retrieval_called}.")
            
        # Verify "heloo" response text
        if q == "heloo" and not retrieval_called:
            if "Hello! I am the ACIS GraphRAG Assistant." not in response.get("answer", "") and "Hello! I am the ACIS GraphRAG Assistant." not in response.get("formatted_answer", ""):
                failed = True
                logger.error(f"'heloo' did not return the expected greeting response. Got: {response.get('answer')}")
        
        results.append({
            "query": q,
            "normalized": n_q,
            "conv_score": conv_score,
            "tech_score": tech_score,
            "retrieval_executed": "YES" if retrieval_called else "NO",
            "expected_retrieval": "YES" if expected_retrieval else "NO",
            "status": "PASSED" if passed else "FAILED"
        })
        
    return not failed, results

def main():
    logger.info("Starting Phase 15.1 fuzzy routing validation...")
    
    success, results = test_routing()
    
    report = "# Phase 15.1 Fuzzy Router Benchmark Report\n\n"
    report += "This report details the routing behavior of the fuzzy conversational gatekeeper, especially against misspelled inputs.\n\n"
    
    report += "## 📊 Query Routing Results\n\n"
    report += "| Original Query | Normalized | Conversational Score | Technical Score | Retrieval Executed | Status |\n"
    report += "| :--- | :--- | :---: | :---: | :---: | :---: |\n"
    for r in results:
        report += f"| `{r['query']}` | `{r['normalized']}` | {r['conv_score']:.1f} | {r['tech_score']:.1f} | **{r['retrieval_executed']}** | **{r['status']}** |\n"
        
    report += "\n## 🛡️ Success Criteria Verification\n\n"
    
    # Specific checks
    heloo_res = next((r for r in results if r["query"] == "heloo"), None)
    if heloo_res:
        report += f"- **`heloo` correctly bypassed retrieval?** {'PASSED' if heloo_res['retrieval_executed'] == 'NO' else 'FAILED'}\n"
    else:
        report += "- **`heloo` test missing.**\n"
        
    mixed_res = next((r for r in results if r["query"] == "hello what is BODY"), None)
    if mixed_res:
        report += f"- **`hello what is BODY` correctly triggered retrieval?** {'PASSED' if mixed_res['retrieval_executed'] == 'YES' else 'FAILED'}\n"
        
    report += f"\n### Overall Status: **{'PASSED' if success else 'FAILED'}**\n"
    
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/reports/router_benchmark_report.md'))
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    logger.info(f"Generated benchmark report at {report_path}")
    
    # Copy to artifacts dir
    artifacts_dir = "C:\\Users\\Dell\\.gemini\\antigravity\\brain\\f4be7305-887d-4ced-85b7-7e8d9e569b25"
    if os.path.exists(artifacts_dir):
        with open(os.path.join(artifacts_dir, 'router_benchmark_report.md'), 'w', encoding='utf-8') as f:
            f.write(report)
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
