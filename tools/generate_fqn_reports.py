import json
import os

def generate_reports():
    print("Generating FQN Migration and Collision Reports...")
    
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "code_base.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    total_classes = 0
    total_structs = 0
    total_enums = 0
    total_typedefs = 0
    total_functions = 0
    total_methods = 0
    
    global_namespace_count = 0
    nested_namespace_count = 0
    namespaces = set()
    
    # Store names to detect collisions: name -> list of dicts with FQN, path, line_number
    name_occurrences = {}
    
    def add_occurrence(name, fqn, path, line_number, entity_type):
        if not name:
            return
        if name not in name_occurrences:
            name_occurrences[name] = []
        name_occurrences[name].append({
            "fqn": fqn,
            "path": path,
            "line_number": line_number,
            "type": entity_type
        })

    for item in data:
        path = item.get("path", "")
        
        for c in item.get("classes", []):
            total_classes += 1
            fqn = c.get("fqn", "")
            name = c.get("name", "")
            add_occurrence(name, fqn, path, c.get("line_number", 0), "Class")
            
            if "::" in fqn:
                nested_namespace_count += 1
                ns_parts = fqn.split("::")[:-1]
                namespaces.add("::".join(ns_parts))
            else:
                global_namespace_count += 1
                
        for s in item.get("structs", []):
            total_structs += 1
            fqn = s.get("fqn", "")
            name = s.get("name", "")
            add_occurrence(name, fqn, path, s.get("line_number", 0), "Struct")
            
            if "::" in fqn:
                nested_namespace_count += 1
                ns_parts = fqn.split("::")[:-1]
                namespaces.add("::".join(ns_parts))
            else:
                global_namespace_count += 1
                
        for e in item.get("enums", []):
            total_enums += 1
            fqn = e.get("fqn", "")
            name = e.get("name", "")
            add_occurrence(name, fqn, path, e.get("line_number", 0), "Enum")
            
            if "::" in fqn:
                nested_namespace_count += 1
                ns_parts = fqn.split("::")[:-1]
                namespaces.add("::".join(ns_parts))
            else:
                global_namespace_count += 1
                
        for t in item.get("typedefs", []):
            total_typedefs += 1
            fqn = t.get("fqn", "")
            name = t.get("name", "")
            add_occurrence(name, fqn, path, t.get("line_number", 0), "Typedef")
            
            if "::" in fqn:
                nested_namespace_count += 1
                ns_parts = fqn.split("::")[:-1]
                namespaces.add("::".join(ns_parts))
            else:
                global_namespace_count += 1
                
        for fn in item.get("functions", []):
            total_functions += 1
            fqn = fn.get("fqn", "")
            name = fn.get("name", "")
            add_occurrence(name, fqn, path, fn.get("line_number", 0), "Function")
            
            if "::" in fqn:
                nested_namespace_count += 1
                ns_parts = fqn.split("::")[:-1]
                namespaces.add("::".join(ns_parts))
            else:
                global_namespace_count += 1
                
        for m in item.get("methods", []):
            total_methods += 1
            fqn = m.get("fqn", "")
            name = m.get("name", "")
            add_occurrence(name, fqn, path, m.get("line_number", 0), "Method")
            
            if "::" in fqn:
                nested_namespace_count += 1
                ns_parts = fqn.split("::")[:-1]
                namespaces.add("::".join(ns_parts))
            else:
                global_namespace_count += 1

    # 1. Generate fqn_migration_report.md
    total_entities = total_classes + total_structs + total_enums + total_typedefs + total_functions + total_methods
    migration_md = f"""# Fully Qualified Name (FQN) Migration Report

## Migration Metrics Summary

- **Total Entities Resolved:** {total_entities}
- **Unique Namespaces Detected:** {len(namespaces)}
- **Global Namespace Entities:** {global_namespace_count} ({global_namespace_count / total_entities * 100:.1f}%)
- **Nested Namespace Entities:** {nested_namespace_count} ({nested_namespace_count / total_entities * 100:.1f}%)

### Breakdown by Entity Type

| Entity Type | Count |
|-------------|-------|
| Classes     | {total_classes} |
| Structs     | {total_structs} |
| Enums       | {total_enums} |
| Typedefs    | {total_typedefs} |
| Functions   | {total_functions} |
| Methods     | {total_methods} |

### Namespaces List
{chr(10).join(sorted(f"- `{ns}`" for ns in list(namespaces)[:30]))}
{'- ... (and more)' if len(namespaces) > 30 else ''}
"""

    # 2. Generate fqn_collision_report.md
    collision_md_entries = ""
    collision_count = 0
    for name, occurrences in sorted(name_occurrences.items()):
        # Filter for unique FQNs/locations
        unique_fqns = set(occ["fqn"] for occ in occurrences)
        if len(unique_fqns) > 1 or len(occurrences) > 1:
            # We have a collision!
            collision_count += 1
            collision_md_entries += f"### Symbol: `{name}` (Occurrences: {len(occurrences)})\n\n"
            collision_md_entries += "| Entity Type | Fully Qualified Name (FQN) | Source File | Line Number |\n"
            collision_md_entries += "|-------------|---------------------------|-------------|-------------|\n"
            for occ in occurrences:
                collision_md_entries += f"| {occ['type']} | `{occ['fqn']}` | `{occ['path']}` | {occ['line_number']} |\n"
            collision_md_entries += "\n"
            
            if collision_count >= 100:  # Cap list to prevent huge files
                collision_md_entries += "### ... (capped at 100 collisions)\n"
                break
                
    collision_md = f"""# Fully Qualified Name (FQN) Collision Report

Total colliding symbols detected: {collision_count}

{collision_md_entries}"""

    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "reports")
    
    migration_path = os.path.join(reports_dir, "fqn_migration_report.md")
    with open(migration_path, "w", encoding="utf-8") as f:
        f.write(migration_md)
    print(f"Migration report written to {migration_path}")
        
    collision_path = os.path.join(reports_dir, "fqn_collision_report.md")
    with open(collision_path, "w", encoding="utf-8") as f:
        f.write(collision_md)
    print(f"Collision report written to {collision_path}")

if __name__ == "__main__":
    generate_reports()
