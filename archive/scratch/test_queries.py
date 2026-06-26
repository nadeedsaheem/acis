"""
End-to-end test of the originally failing queries.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from retriever import semantic_search

test_queries = ["spa", "what is spaposition", "SPAposition", "position class"]

for q in test_queries:
    print()
    print("=" * 60)
    print(f"Query: '{q}'")
    results = semantic_search(q, top_k=5)
    hits = results.get('results', [])
    if not hits:
        print("  [FAIL] NO RESULTS FOUND")
    else:
        print(f"  [OK] {len(hits)} results found:")
        for i, r in enumerate(hits[:3]):
            print(f"    {i+1}. [{r['entity_type']}] {r['entity_name']} (score={r['score']:.4f})")
            if r.get('documentation'):
                print(f"       Doc: {r['documentation'][:80]}...")

print("\n\nTest complete.")
