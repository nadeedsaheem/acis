import json
import hashlib
from collections import defaultdict

def generate_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

with open('code_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# emulate build_graph.py
name_to_id = {}
class_nodes = set()
for item in data:
    path = item.get('path')
    if not path: continue
    for cls in item.get('classes', []):
        name = cls.get('name')
        if name:
            class_id = f"{path}::{name}"
            class_nodes.add(class_id)
            if name not in name_to_id:
                name_to_id[name] = class_id

methods_created = set()
method_edges = set()

external_classes = set()
internal_classes_matched = set()

functions_missing = 0
functions_created = set()
skipped_funcs = 0
missing_signatures = 0
malformed_signatures = 0
func_duplicate_ids = set()
all_func_ids = []

method_details = []

for item in data:
    path = item.get('path')
    if not path: continue
    
    # functions
    for fn in item.get('functions', []):
        name = fn.get('name')
        if name:
            params = fn.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            signature = f"{name}({param_str})"
            
            if not param_str and params: # malformed if params exists but type is empty? we can check later
                pass
            
            raw_id = f"{path}::{name}::{signature}"
            func_id = generate_hash(raw_id)
            all_func_ids.append(func_id)
            functions_created.add(func_id)

    # methods
    for md in item.get('methods', []):
        name = md.get('name')
        class_name = md.get('class')
        if name and class_name:
            params = md.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            signature = f"{name}({param_str})"
            
            raw_id = f"{path}::{class_name}::{name}::{signature}"
            method_id = generate_hash(raw_id)
            
            methods_created.add(method_id)
            
            if class_name in name_to_id:
                class_id = name_to_id[class_name]
                if class_id in class_nodes:
                    method_edges.add((class_id, method_id))
                    internal_classes_matched.add(class_id)
                else:
                    method_details.append({
                        'method_id': method_id,
                        'method_name': name,
                        'class_name': class_name,
                        'reason': 'Class ID found in name_to_id but not in Class nodes (Should be impossible)'
                    })
            else:
                external_classes.add(class_name)
                method_edges.add((class_name, method_id))
                method_details.append({
                    'method_id': method_id,
                    'method_name': name,
                    'class_name': class_name,
                    'reason': 'Class name not found in name_to_id'
                })

print(f"Classes: {len(class_nodes)}")
print(f"ExternalClasses generated: {len(external_classes)}")
print(f"Functions created (unique): {len(functions_created)}")
print(f"Total function definitions seen: {len(all_func_ids)}")
print(f"Methods created (unique): {len(methods_created)}")
print(f"Method edges (unique): {len(method_edges)}")

import collections
func_id_counts = collections.Counter(all_func_ids)
duplicates = sum(1 for v in func_id_counts.values() if v > 1)
total_duplicate_loss = sum(v - 1 for v in func_id_counts.values() if v > 1)
print(f"Function Duplicate IDs: {duplicates} (causing loss of {total_duplicate_loss} nodes)")

# Output a sample of external classes
print("Sample external classes:")
print(list(external_classes)[:20])
