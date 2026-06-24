import os
import json
import sys

def validate():
    original_file = "code_base.json"
    clean_file = "code_base_clean.json"

    if not os.path.exists(original_file):
        print(f"Error: Original file '{original_file}' not found.")
        sys.exit(1)
    if not os.path.exists(clean_file):
        print(f"Error: Cleaned file '{clean_file}' not found.")
        sys.exit(1)

    print("Loading datasets for validation...")
    with open(original_file, "r", encoding="utf-8") as f:
        original = json.load(f)
    with open(clean_file, "r", encoding="utf-8") as f:
        clean = json.load(f)

    # 1. Total records check
    orig_files = len(original)
    clean_files = len(clean)
    
    print("\n==================================================")
    print("DATASET VALIDATION REPORT")
    print("==================================================")

    checks_passed = True

    def report_check(name, orig_val, clean_val):
        nonlocal checks_passed
        if orig_val == clean_val:
            print(f"[PASS] {name:<30} | Original: {orig_val:<6} | Clean: {clean_val:<6}")
        else:
            print(f"[FAIL] {name:<30} | Original: {orig_val:<6} | Clean: {clean_val:<6}")
            checks_passed = False

    report_check("File records count", orig_files, clean_files)

    # Accumulate entities
    orig_counts = {
        "classes": 0, "structs": 0, "enums": 0, "typedefs": 0,
        "namespaces": 0, "includes": 0, "methods": 0, "functions": 0,
        "inheritance": 0
    }
    clean_counts = {
        "classes": 0, "structs": 0, "enums": 0, "typedefs": 0,
        "namespaces": 0, "includes": 0, "methods": 0, "functions": 0,
        "inheritance": 0
    }

    for item in original:
        orig_counts["classes"] += len(item.get("classes", []))
        orig_counts["structs"] += len(item.get("structs", []))
        orig_counts["enums"] += len(item.get("enums", []))
        orig_counts["typedefs"] += len(item.get("typedefs", []))
        orig_counts["namespaces"] += len(item.get("namespaces", []))
        orig_counts["includes"] += len(item.get("includes", []))
        orig_counts["methods"] += len(item.get("methods", []))
        orig_counts["functions"] += len(item.get("functions", []))
        orig_counts["inheritance"] += len(item.get("inheritance", []))

    for item in clean:
        clean_counts["classes"] += len(item.get("classes", []))
        clean_counts["structs"] += len(item.get("structs", []))
        clean_counts["enums"] += len(item.get("enums", []))
        clean_counts["typedefs"] += len(item.get("typedefs", []))
        clean_counts["namespaces"] += len(item.get("namespaces", []))
        clean_counts["includes"] += len(item.get("includes", []))
        clean_counts["methods"] += len(item.get("methods", []))
        clean_counts["functions"] += len(item.get("functions", []))
        clean_counts["inheritance"] += len(item.get("inheritance", []))

    # Verify counts
    for entity in sorted(orig_counts.keys()):
        report_check(f"{entity.capitalize()} count", orig_counts[entity], clean_counts[entity])

    print("==================================================")
    if checks_passed:
        print("SUCCESS: Cleaned dataset matches original dataset perfectly.")
        sys.exit(0)
    else:
        print("ERROR: Mismatches detected between original and cleaned dataset.")
        sys.exit(1)

if __name__ == "__main__":
    validate()
