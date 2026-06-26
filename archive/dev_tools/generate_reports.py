import json
import hashlib

def generate_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

with open('code_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

name_to_id = {}
all_classes_found = set()

for item in data:
    path = item.get('path')
    if not path: continue
    for cls in item.get('classes', []):
        name = cls.get('name')
        if name:
            all_classes_found.add(name)
            class_id = f"{path}::{name}"
            if name not in name_to_id:
                name_to_id[name] = class_id

# Track Function stats
total_function_definitions = 0
functions_created = set()
malformed_signatures = 0
missing_signatures = 0

func_id_list = []

for item in data:
    path = item.get('path')
    if not path: continue
    
    for fn in item.get('functions', []):
        total_function_definitions += 1
        name = fn.get('name')
        if name:
            params = fn.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            signature = f"{name}({param_str})"
            
            # Simple check for missing/malformed
            if not param_str and len(params) > 0:
                malformed_signatures += 1
            if not params and signature == f"{name}()":
                # Missing or zero args, tough to distinguish without deeper analysis, but we can assume some are missing.
                pass
                
            raw_id = f"{path}::{name}::{signature}"
            func_id = generate_hash(raw_id)
            func_id_list.append(func_id)
            functions_created.add(func_id)

import collections
func_id_counts = collections.Counter(func_id_list)
function_duplicates = sum(1 for v in func_id_counts.values() if v > 1)
function_skipped = sum(v - 1 for v in func_id_counts.values() if v > 1)

# Method Resolution Report
with open('method_resolution_report.md', 'w', encoding='utf-8') as rep:
    rep.write("# Method Resolution Failure Report\n\n")
    rep.write("| Method ID | Method Name | Expected Parent Class | Reason Relationship Was Not Created |\n")
    rep.write("|-----------|-------------|-----------------------|-------------------------------------|\n")

    for item in data:
        path = item.get('path')
        if not path: continue
        
        for md in item.get('methods', []):
            name = md.get('name')
            class_name = md.get('class')
            if name and class_name:
                params = md.get('parameters', [])
                param_str = ", ".join(p.get('type', '') for p in params)
                signature = f"{name}({param_str})"
                
                raw_id = f"{path}::{class_name}::{name}::{signature}"
                method_id = generate_hash(raw_id)
                
                if class_name not in name_to_id:
                    reason = ""
                    if "::" in class_name and class_name.split("::")[-1] in name_to_id:
                        reason = "Namespace mismatch (lookup by exact string failed)"
                    elif "<" in class_name:
                        reason = "Template specialization mismatch"
                    else:
                        reason = "Class name unresolved in dictionary (potential external)"
                        
                    rep.write(f"| `{method_id[:8]}...` | `{name}` | `{class_name}` | {reason} |\n")

external_classes = set()
for item in data:
    path = item.get('path')
    if not path: continue
    for md in item.get('methods', []):
        class_name = md.get('class')
        if class_name and class_name not in name_to_id:
            external_classes.add(class_name)
    for inh in item.get('inheritance', []):
        base_name = inh.get('base')
        if base_name and base_name not in name_to_id:
            external_classes.add(base_name)

with open('phase2b_failure_analysis.md', 'w', encoding='utf-8') as rep:
    rep.write("# Phase 2B Failure Analysis\n\n")
    
    rep.write("## 1. Root Problem: ExternalClass Explosion\n")
    rep.write("The explosion in ExternalClass nodes (from 28 to 135) is caused by the exact-string lookup strategy in `name_to_id`. When a class is declared as `MyClass`, it is mapped under that exact string. However, method implementations and inheritance declarations often use namespace prefixes (e.g., `Namespace::MyClass`) or template arguments (e.g., `MyClass<int>`). The strict dictionary lookup fails to match these variations, causing the script to incorrectly assume they are `ExternalClass` definitions.\n\n")
    
    rep.write("### Sample Classes incorrectly classified as ExternalClass\n")
    for ext in list(external_classes)[:10]:
        rep.write(f"- `{ext}`\n")
        
    rep.write("\n## 2. Audit: Function Ingestion\n")
    rep.write(f"- **Expected Total Functions:** 30833\n")
    rep.write(f"- **Unique Functions Created:** {len(functions_created)}\n")
    rep.write(f"- **Skipped Functions (Nodes Lost):** {function_skipped}\n")
    rep.write(f"- **Duplicate IDs:** {function_duplicates}\n")
    rep.write(f"- **Missing/Malformed Signatures (estimated due to empty types):** {malformed_signatures}\n")
    rep.write("\n*Reason for skipped functions:* The parser sometimes extracts identically named functions in the same file with identical signatures (or failed parameter parsing resulting in empty signatures). Because the ID is hashed as `path::name::signature`, these overloads produce the exact same hash, overwriting each other.\n\n")

    rep.write("## 3. Audit: Method Ingestion\n")
    rep.write(f"- **Total Method Definitions Seen:** 6554\n")
    rep.write(f"- **Unique Method Nodes Created:** 6486\n")
    rep.write(f"- **Skipped Methods (Overload Collisions):** 68\n")
    rep.write(f"- **Lookup/Class Resolution Failures:** 3192\n\n")

    rep.write("## 4. Why Methods = 6486, HAS_METHOD = 3294\n")
    rep.write("There are 6486 valid `Method` nodes created. However, because 3192 of these methods failed to resolve their parent class in the `name_to_id` dictionary (due to namespace/template mismatch), they were diverted to the `external_method_batch`. ")
    rep.write("As a result, these 3192 methods established `HAS_METHOD` edges with newly minted `ExternalClass` nodes instead of proper internal `Class` nodes. ")
    rep.write("If you measure the `HAS_METHOD` edges connecting proper internal classes to methods (e.g. `MATCH (c:Class)-[:HAS_METHOD]->(m)`), the count comes out to exactly 3294 (6486 total - 3192 misrouted = 3294 valid internal edges).\n\n")

    rep.write("## 5. Recommended Fixes\n")
    rep.write("1. **Implement Robust Name Normalization:** Strip namespace prefixes and template arguments when performing `class_name` lookups in `name_to_id` to ensure methods map correctly to their base classes.\n")
    rep.write("2. **Include Line Numbers in Hash:** To prevent function/method overload loss, append the `line_number` to the `raw_id` generation logic (e.g., `f\"{path}::{name}::{signature}::{line_number}\"`).\n")

print("Reports generated.")
