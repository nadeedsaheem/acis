import json
from collections import defaultdict

def analyze():
    with open('code_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Gather all class IDs that actually exist from Phase 1.1 logic
    existing_class_ids = set()
    for file_obj in data:
        path = file_obj.get('path', 'unknown')
        for cls in file_obj.get('classes', []):
            name = cls.get('name')
            if name:
                existing_class_ids.add(f"{path}::{name}")

    method_collisions = defaultdict(list)
    func_collisions = defaultdict(list)
    
    unique_method_names = set()
    unique_method_signatures = set()
    
    unique_func_names = set()
    unique_func_signatures = set()
    
    methods_skipped_due_to_class = 0
    methods_created = set()
    
    for file_obj in data:
        path = file_obj.get('path', 'unknown')
        
        # Methods
        for md in file_obj.get('methods', []):
            c_name = md.get('class')
            m_name = md.get('name')
            if not c_name or not m_name: continue
            
            unique_method_names.add(m_name)
            
            # Reconstruct signature: name(type1, type2)
            params = md.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            sig = f"{m_name}({param_str})"
            unique_method_signatures.add(sig)
            
            # The ID we used in build_graph.py
            method_id = f"{path}::{c_name}::{m_name}"
            
            class_id = f"{path}::{c_name}"
            
            # Store for collision report
            method_collisions[method_id].append({
                'class': c_name,
                'method': m_name,
                'path': path,
                'signature': sig
            })
            
            # Simulate Neo4j behavior
            if class_id not in existing_class_ids:
                methods_skipped_due_to_class += 1
            else:
                methods_created.add(method_id)
                
        # Functions
        for fn in file_obj.get('functions', []):
            f_name = fn.get('name')
            if not f_name: continue
            
            unique_func_names.add(f_name)
            
            params = fn.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            sig = f"{f_name}({param_str})"
            unique_func_signatures.add(sig)
            
            func_id = f"{path}::{f_name}"
            func_collisions[func_id].append({
                'function': f_name,
                'path': path,
                'signature': sig
            })

    print(f"Total methods parsed: {sum(len(v) for v in method_collisions.values())}")
    print(f"Methods skipped due to missing class in same file: {methods_skipped_due_to_class}")
    print(f"Method nodes created in Neo4j (simulated): {len(methods_created)}")
    
    # Generate method collision report
    md_report = "# Method Collision Report\n\n"
    
    # Only report actual overloads (occurrences > 1)
    overloads = {k: v for k, v in method_collisions.items() if len(v) > 1}
    
    md_report += "## Method Overloads Collapsed\n"
    md_report += "The following methods share the same `file_path::class_name::method_name` identifier but have different signatures (overloads). Neo4j MERGE collapsed them into single nodes.\n\n"
    
    for m_id, instances in sorted(overloads.items(), key=lambda x: len(x[1]), reverse=True):
        c_name = instances[0]['class']
        m_name = instances[0]['method']
        p = instances[0]['path']
        md_report += f"### Class: `{c_name}` | Method: `{m_name}`\n"
        md_report += f"- **File Path:** `{p}`\n"
        md_report += f"- **Overload Count:** {len(instances)}\n"
        md_report += "- **Signatures:**\n"
        for inst in instances:
            md_report += f"  - `{inst['signature']}`\n"
        md_report += "\n"
        
    with open('method_collision_report.md', 'w', encoding='utf-8') as f:
        f.write(md_report)
        
    print("\n--- Stats ---")
    print(f"Unique method names: {len(unique_method_names)}")
    print(f"Unique method signatures: {len(unique_method_signatures)}")
    print(f"Unique function names: {len(unique_func_names)}")
    print(f"Unique function signatures: {len(unique_func_signatures)}")

if __name__ == '__main__':
    analyze()
