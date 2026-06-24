import json
import os
import re

def main():
    print("Loading code_base.json...")
    with open("code_base.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    REPO_ROOT = r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS"
    INCLUDE_DIR = os.path.join(REPO_ROOT, "include")
    
    # 1. Coverage Audit
    valid_exts = {".h", ".hxx", ".hpp", ".hh", ".err"}
    actual_files = set()
    for root, _, files in os.walk(INCLUDE_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                rel = os.path.relpath(os.path.join(root, file), REPO_ROOT).replace("\\", "/")
                actual_files.add(rel)
                
    dataset_files = [d["path"] for d in dataset]
    dataset_files_set = set(dataset_files)
    
    missing_files = actual_files - dataset_files_set
    duplicates = len(dataset_files) - len(dataset_files_set)
    
    # 2. Entity Extraction
    # 3. Macro Handling
    # 4. Doc Audit
    # 8. Prod Dataset Quality
    
    counts = {
        "classes": 0, "structs": 0, "enums": 0, "typedefs": 0, "namespaces": 0,
        "functions": 0, "methods": 0, "inheritance": 0, "includes": 0
    }
    
    doc_counts = {"functions": 0, "methods": 0, "classes": 0}
    doc_invalid = 0
    
    orphan_methods = []
    orphan_inheritance = []
    empty_names = []
    invalid_line_numbers = []
    
    all_classes_and_structs = set()
    
    for item in dataset:
        all_classes_and_structs.update([c["name"] for c in item.get("classes", [])])
        all_classes_and_structs.update([s["name"] for s in item.get("structs", [])])
        
        counts["classes"] += len(item.get("classes", []))
        counts["structs"] += len(item.get("structs", []))
        counts["enums"] += len(item.get("enums", []))
        counts["typedefs"] += len(item.get("typedefs", []))
        counts["namespaces"] += len(item.get("namespaces", []))
        counts["functions"] += len(item.get("functions", []))
        counts["methods"] += len(item.get("methods", []))
        counts["inheritance"] += len(item.get("inheritance", []))
        counts["includes"] += len(item.get("includes", []))
        
        # Docs check
        for f in item.get("functions", []):
            if "name" not in f or not f["name"]: empty_names.append({"file": item["path"], "type": "function"})
            if "line_number" not in f or f["line_number"] <= 0: invalid_line_numbers.append({"file": item["path"], "type": "function", "name": f.get("name")})
            if f.get("documentation"):
                doc_counts["functions"] += 1
                doc = f["documentation"]
                if "copyright" in doc.lower() or "license" in doc.lower() or doc.strip().startswith("/*") and "*" * 20 in doc:
                    doc_invalid += 1
                    
        for m in item.get("methods", []):
            if "name" not in m or not m["name"]: empty_names.append({"file": item["path"], "type": "method"})
            if "line_number" not in m or m["line_number"] <= 0: invalid_line_numbers.append({"file": item["path"], "type": "method", "name": m.get("name")})
            if not m.get("class"):
                orphan_methods.append({"file": item["path"], "method": m.get("name")})
            if m.get("documentation"):
                doc_counts["methods"] += 1
                doc = m["documentation"]
                if "copyright" in doc.lower() or "license" in doc.lower() or doc.strip().startswith("/*") and "*" * 20 in doc:
                    doc_invalid += 1
                    
        for c in item.get("classes", []):
            if "name" not in c or not c["name"]: empty_names.append({"file": item["path"], "type": "class"})
            if "line_number" not in c or c["line_number"] <= 0: invalid_line_numbers.append({"file": item["path"], "type": "class", "name": c.get("name")})
            if c.get("documentation"):
                doc_counts["classes"] += 1
                doc = c["documentation"]
                if "copyright" in doc.lower() or "license" in doc.lower() or doc.strip().startswith("/*") and "*" * 20 in doc:
                    doc_invalid += 1
                    
    for item in dataset:
        for inh in item.get("inheritance", []):
            # If inheritance points to something we don't know, it's orphan? No, could be external
            if inh["class"] not in all_classes_and_structs:
                orphan_inheritance.append({"file": item["path"], "class": inh["class"], "base": inh["base"]})
                
    print(f"Total Source: {len(actual_files)}")
    print(f"Total Dataset: {len(dataset)}")
    print(f"Missing: {len(missing_files)}")
    print(f"Duplicates: {duplicates}")
    print("--- COUNTS ---")
    for k, v in counts.items(): print(f"{k}: {v}")
    print("--- DOCS ---")
    for k, v in doc_counts.items(): print(f"{k}: {v}")
    print(f"Invalid docs: {doc_invalid}")
    print("--- ISSUES ---")
    print(f"Orphan methods: {len(orphan_methods)}")
    print(f"Orphan inheritance (class not found): {len(orphan_inheritance)}")
    print(f"Empty names: {len(empty_names)}")
    print(f"Invalid line numbers: {len(invalid_line_numbers)}")
    
if __name__ == "__main__":
    main()
