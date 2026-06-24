import json
import re
import os

def run_audit():
    with open("code_base.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    # Stats containers
    schema_errors = []
    
    entity_stats = {"classes": 0, "structs": 0, "enums": 0, "typedefs": 0, "namespaces": 0}
    missing_names = 0
    missing_lines = 0
    malformed_entities = 0
    
    function_stats = {"total": 0, "empty_names": 0, "invalid_lines": 0}
    method_stats = {"total": 0, "orphans": 0, "empty_names": 0, "invalid_lines": 0, "missing_class": 0}
    
    param_stats = {"total": 0, "malformed": 0, "missing_type": 0}
    
    enum_stats = {"total": 0, "with_values": 0, "without_values": 0, "empty_values": 0, "duplicate_values": 0}
    
    inheritance_stats = {"total": 0, "self_inheritance": 0, "duplicate_edges": 0, "malformed_edges": 0, "missing_names": 0}
    
    doc_stats = {"total_docs": 0, "html_leaks": 0}
    
    # Trackers for uniqueness
    all_edges = set()
    
    for record in dataset:
        # Part 1 Schema check
        expected_keys = {"file", "path", "classes", "structs", "enums", "typedefs", "namespaces", "functions", "methods", "includes", "inheritance"}
        actual_keys = set(record.keys())
        if actual_keys != expected_keys:
            schema_errors.append(f"File {record.get('file')} schema mismatch. Missing: {expected_keys - actual_keys}, Extra: {actual_keys - expected_keys}")
            
        # Part 2 Entities
        for c in record.get("classes", []):
            entity_stats["classes"] += 1
            if not c.get("name"): missing_names += 1
            if not c.get("line_number"): missing_lines += 1
            if "name" not in c or "line_number" not in c or "documentation" not in c: malformed_entities += 1
            
        for s in record.get("structs", []):
            entity_stats["structs"] += 1
            if not s.get("name"): missing_names += 1
            if not s.get("line_number"): missing_lines += 1
            if "name" not in s or "line_number" not in s or "documentation" not in s: malformed_entities += 1
            
        for e in record.get("enums", []):
            entity_stats["enums"] += 1
            if not e.get("name"): missing_names += 1
            if not e.get("line_number"): missing_lines += 1
            if "name" not in e or "line_number" not in e or "documentation" not in e or "values" not in e: malformed_entities += 1
            
            if "values" in e:
                vals = e["values"]
                if not vals:
                    enum_stats["without_values"] += 1
                else:
                    enum_stats["with_values"] += 1
                    if len(vals) != len(set(vals)): enum_stats["duplicate_values"] += 1
                    if any(not v for v in vals): enum_stats["empty_values"] += 1
                    
        for t in record.get("typedefs", []):
            entity_stats["typedefs"] += 1
            if not t.get("name"): missing_names += 1
            if not t.get("line_number"): missing_lines += 1
            if "name" not in t or "line_number" not in t or "documentation" not in t: malformed_entities += 1
            
        for ns in record.get("namespaces", []):
            entity_stats["namespaces"] += 1
            if not ns.get("name"): missing_names += 1
            if not ns.get("line_number"): missing_lines += 1
            if "name" not in ns or "line_number" not in ns: malformed_entities += 1
            
        # Part 3 Functions
        for f in record.get("functions", []):
            function_stats["total"] += 1
            if not f.get("name"): function_stats["empty_names"] += 1
            if not f.get("line_number"): function_stats["invalid_lines"] += 1
            
            if f.get("documentation"):
                doc_stats["total_docs"] += 1
                doc = f["documentation"]
                if re.search(r'<(br|b|i|/b|/i)>', doc, re.IGNORECASE):
                    doc_stats["html_leaks"] += 1
            
            for p in f.get("parameters", []):
                param_stats["total"] += 1
                if not isinstance(p, dict) or "type" not in p or "name" not in p:
                    param_stats["malformed"] += 1
                elif not p["type"]:
                    param_stats["missing_type"] += 1
                    
        # Part 4 Methods
        for m in record.get("methods", []):
            method_stats["total"] += 1
            if not m.get("name"): method_stats["empty_names"] += 1
            if not m.get("line_number"): method_stats["invalid_lines"] += 1
            if "class" not in m: 
                method_stats["missing_class"] += 1
                method_stats["orphans"] += 1
            elif not m["class"]:
                method_stats["orphans"] += 1
                
            if m.get("documentation"):
                doc_stats["total_docs"] += 1
                doc = m["documentation"]
                if re.search(r'<(br|b|i|/b|/i)>', doc, re.IGNORECASE):
                    doc_stats["html_leaks"] += 1
                    
            for p in m.get("parameters", []):
                param_stats["total"] += 1
                if not isinstance(p, dict) or "type" not in p or "name" not in p:
                    param_stats["malformed"] += 1
                elif not p["type"]:
                    param_stats["missing_type"] += 1
                    
        for c in record.get("classes", []) + record.get("structs", []) + record.get("enums", []) + record.get("typedefs", []):
            if c.get("documentation"):
                doc_stats["total_docs"] += 1
                doc = c["documentation"]
                if re.search(r'<(br|b|i|/b|/i)>', doc, re.IGNORECASE):
                    doc_stats["html_leaks"] += 1
                    
        # Part 7 Inheritance
        for inh in record.get("inheritance", []):
            inheritance_stats["total"] += 1
            c_name = inh.get("class")
            b_name = inh.get("base")
            
            if not c_name or not b_name:
                inheritance_stats["missing_names"] += 1
            if c_name == b_name:
                inheritance_stats["self_inheritance"] += 1
            
            edge = (c_name, b_name)
            if edge in all_edges:
                inheritance_stats["duplicate_edges"] += 1
            all_edges.add(edge)
            
            if "class" not in inh or "base" not in inh:
                inheritance_stats["malformed_edges"] += 1

    schema_compliance = 100.0 if not schema_errors else ((len(dataset) - len(schema_errors)) / len(dataset) * 100)
    param_acc = 100.0 if param_stats["total"] == 0 else ((param_stats["total"] - param_stats["malformed"] - param_stats["missing_type"]) / param_stats["total"] * 100)
    inh_acc = 100.0 if inheritance_stats["total"] == 0 else ((inheritance_stats["total"] - inheritance_stats["self_inheritance"] - inheritance_stats["duplicate_edges"] - inheritance_stats["malformed_edges"] - inheritance_stats["missing_names"]) / inheritance_stats["total"] * 100)
    doc_clean = 100.0 if doc_stats["total_docs"] == 0 else ((doc_stats["total_docs"] - doc_stats["html_leaks"]) / doc_stats["total_docs"] * 100)

    report = "==================================================\n"
    report += "FINAL DATASET CERTIFICATION AUDIT\n"
    report += "==================================================\n\n"
    
    report += "PART 1 — Schema Consistency\n"
    report += f"Schema Compliance: {schema_compliance:.2f}%\n"
    if schema_errors:
        report += f"Errors found: {len(schema_errors)}\n"
    report += "\n"
    
    report += "PART 2 — Entity Integrity\n"
    report += f"Classes: {entity_stats['classes']}, Structs: {entity_stats['structs']}, Enums: {entity_stats['enums']}, Typedefs: {entity_stats['typedefs']}, Namespaces: {entity_stats['namespaces']}\n"
    report += f"Missing names: {missing_names}\n"
    report += f"Missing line numbers: {missing_lines}\n"
    report += f"Malformed entities: {malformed_entities}\n\n"
    
    report += "PART 3 — Function Integrity\n"
    report += f"Total Functions: {function_stats['total']}\n"
    report += f"Empty names: {function_stats['empty_names']}\n"
    report += f"Invalid line numbers: {function_stats['invalid_lines']}\n\n"
    
    report += "PART 4 — Method Integrity\n"
    report += f"Total Methods: {method_stats['total']}\n"
    report += f"Missing class owner field: {method_stats['missing_class']}\n"
    report += f"Orphan methods (no class): {method_stats['orphans']}\n"
    report += f"Empty names: {method_stats['empty_names']}\n"
    report += f"Invalid line numbers: {method_stats['invalid_lines']}\n\n"
    
    report += "PART 5 — Parameter Quality\n"
    report += f"Total Parameters Checked: {param_stats['total']}\n"
    report += f"Malformed structures: {param_stats['malformed']}\n"
    report += f"Missing types: {param_stats['missing_type']}\n"
    report += f"Parameter Parsing Accuracy: {param_acc:.2f}%\n\n"
    
    report += "PART 6 — Enum Validation\n"
    report += f"Enums with values: {enum_stats['with_values']}\n"
    report += f"Enums without values: {enum_stats['without_values']} (Forward Declarations)\n"
    report += f"Malformed enums (empty/duplicate values): {enum_stats['empty_values'] + enum_stats['duplicate_values']}\n\n"
    
    report += "PART 7 — Inheritance Graph Validation\n"
    report += f"Total Edges: {inheritance_stats['total']}\n"
    report += f"Self-inheritance: {inheritance_stats['self_inheritance']}\n"
    report += f"Duplicate edges: {inheritance_stats['duplicate_edges']}\n"
    report += f"Malformed edges: {inheritance_stats['malformed_edges']}\n"
    report += f"Missing class names: {inheritance_stats['missing_names']}\n"
    report += f"Inheritance Integrity: {inh_acc:.2f}%\n\n"
    
    report += "PART 8 — Documentation Quality\n"
    report += f"Total Docs Parsed: {doc_stats['total_docs']}\n"
    report += f"HTML Tag Leaks: {doc_stats['html_leaks']}\n"
    report += f"Documentation Cleanliness: {doc_clean:.2f}%\n\n"
    
    # Calculate overall score roughly
    score = (schema_compliance + param_acc + inh_acc + doc_clean + (100 if malformed_entities==0 else 0) + (100 if method_stats["orphans"]==0 else 0)) / 6
    
    with open("audit_results.txt", "w", encoding="utf-8") as f:
        f.write(report)
        f.write(f"Overall Dataset Quality Score: {score:.2f}\n")

if __name__ == "__main__":
    run_audit()
