import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

import asyncio
from retrieval.query_normalizer import normalize_query

def run_tests():
    print("Running Phase 9.2 Validation: Query Normalization")
    print("------------------------------------------------")
    
    # Target entities that exist in DB
    entities_in_db = [
        "SPAposition",
        "ENTITY",
        "BODY",
        "FACE",
        "outcome"
    ]
    
    # Entities that don't exist in DB
    entities_not_in_db = [
        "TopoDS_Shape",
        "gp_Pnt"
    ]
    
    success = True
    print("\n[Entity Lookup Tests]")
    for e in entities_in_db:
        norm = normalize_query(e)
        expected = f"What is {e}?"
        if norm == expected:
            print(f"PASS: '{e}' -> '{norm}'")
        else:
            print(f"FAIL: '{e}' -> '{norm}' (Expected: '{expected}')")
            success = False
            
    for e in entities_not_in_db:
        norm = normalize_query(e)
        if norm == e:
            print(f"PASS: '{e}' -> UNCHANGED (Not in DB, avoids false positive)")
        else:
            print(f"FAIL: '{e}' -> '{norm}' (Expected: UNCHANGED)")
            success = False
            
    # Regression tests
    print("\n[Regression Tests]")
    regressions = [
        "How does variable radius blending work?",
        "How are model changes tracked?",
        "Which functions return outcome?"
    ]
    for q in regressions:
        norm = normalize_query(q)
        if norm == q:
            print(f"PASS: '{q}' -> UNCHANGED")
        else:
            print(f"FAIL: '{q}' -> '{norm}' (Expected: UNCHANGED)")
            success = False
            
    # Hallucination tests
    print("\n[Hallucination Protection Tests]")
    hallucinations = [
        "QuantumTeleportationEngine",
        "LunarNavigationSubsystem"
    ]
    for h in hallucinations:
        norm = normalize_query(h)
        if norm == h:
            print(f"PASS: '{h}' -> UNCHANGED (Not in DB)")
        else:
            print(f"FAIL: '{h}' -> '{norm}' (Expected: UNCHANGED)")
            success = False

    if success:
        print("\nALL TESTS PASSED: Query Normalizer meets all criteria.")
    else:
        print("\nSOME TESTS FAILED.")
        
if __name__ == "__main__":
    run_tests()
