from retriever import semantic_search

queries = [
    "How does variable radius blending work?",
    "Methods related to SPAposition",
    "What functions return outcome?",
    "Entity journaling operations",
    "How are smooth edge transitions generated?"
]

for q in queries:
    print("=" * 80)
    print("QUERY:", q)

    results = semantic_search(q)

    print("RESULT COUNT:", len(results.get("results", [])))

    for r in results.get("results", [])[:3]:
        print("\nENTITY:", r.get("entity_name"))
        print("TYPE:", r.get("entity_type"))
        print("SCORE:", r.get("score"))