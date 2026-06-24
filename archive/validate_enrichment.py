import json

def validate():
    with open("code_base.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    stats = {
        "classes": {"total": 0, "has_line": 0},
        "structs": {"total": 0, "has_line": 0},
        "enums": {"total": 0, "has_line": 0, "has_values": 0},
        "typedefs": {"total": 0, "has_line": 0},
        "namespaces": {"total": 0, "has_line": 0},
        "functions": {"total": 0, "structured_params": 0},
        "methods": {"total": 0, "structured_params": 0}
    }
    
    for item in data:
        for c in item.get("classes", []):
            stats["classes"]["total"] += 1
            if "line_number" in c: stats["classes"]["has_line"] += 1
            
        for s in item.get("structs", []):
            stats["structs"]["total"] += 1
            if "line_number" in s: stats["structs"]["has_line"] += 1
            
        for e in item.get("enums", []):
            stats["enums"]["total"] += 1
            if "line_number" in e: stats["enums"]["has_line"] += 1
            if "values" in e and len(e["values"]) > 0: stats["enums"]["has_values"] += 1
            
        for t in item.get("typedefs", []):
            stats["typedefs"]["total"] += 1
            if "line_number" in t: stats["typedefs"]["has_line"] += 1
            
        for ns in item.get("namespaces", []):
            stats["namespaces"]["total"] += 1
            if "line_number" in ns: stats["namespaces"]["has_line"] += 1
            
        for f in item.get("functions", []):
            stats["functions"]["total"] += 1
            has_structured = True
            for p in f.get("parameters", []):
                if not isinstance(p, dict) or "type" not in p or "name" not in p:
                    has_structured = False
                    break
            if has_structured: stats["functions"]["structured_params"] += 1
            
        for m in item.get("methods", []):
            stats["methods"]["total"] += 1
            has_structured = True
            for p in m.get("parameters", []):
                if not isinstance(p, dict) or "type" not in p or "name" not in p:
                    has_structured = False
                    break
            if has_structured: stats["methods"]["structured_params"] += 1

    report = "==================================================\n"
    report += "METADATA ENRICHMENT VALIDATION REPORT\n"
    report += "==================================================\n\n"
    
    def format_stat(name, total, count, suffix="with line numbers"):
        pct = (count / total * 100) if total > 0 else 100.0
        return f"{name:<20}: {count}/{total} {suffix} ({pct:.1f}%)\n"

    report += format_stat("Classes", stats["classes"]["total"], stats["classes"]["has_line"])
    report += format_stat("Structs", stats["structs"]["total"], stats["structs"]["has_line"])
    report += format_stat("Enums", stats["enums"]["total"], stats["enums"]["has_line"])
    report += format_stat("Typedefs", stats["typedefs"]["total"], stats["typedefs"]["has_line"])
    report += format_stat("Namespaces", stats["namespaces"]["total"], stats["namespaces"]["has_line"])
    report += "\n"
    report += format_stat("Functions", stats["functions"]["total"], stats["functions"]["structured_params"], "with structured params")
    report += format_stat("Methods", stats["methods"]["total"], stats["methods"]["structured_params"], "with structured params")
    report += "\n"
    report += format_stat("Enums (Values)", stats["enums"]["total"], stats["enums"]["has_values"], "with extracted values")
    
    with open("enrichment_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
        
    print(report)

if __name__ == "__main__":
    validate()
