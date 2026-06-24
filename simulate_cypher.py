import json
import hashlib

def generate_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

with open('code_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

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

internal_method_batch = []
external_method_batch = []
function_batch = []

skipped_methods = 0

for item in data:
    path = item.get('path')
    if not path: continue
    
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
            
            if class_name in name_to_id:
                class_id = name_to_id[class_name]
                internal_method_batch.append({
                    'id': method_id,
                    'path': path,
                    'class_id': class_id,
                    'name': name,
                    'class_name': class_name,
                    'signature': signature
                })
            else:
                external_method_batch.append({
                    'id': method_id,
                    'path': path,
                    'class_name': class_name,
                    'name': name,
                    'signature': signature
                })

# Simulate Cypher for Methods
method_nodes = set()
has_method_edges = set()

# Internal
for row in internal_method_batch:
    c_id = row['class_id']
    if c_id in class_nodes:
        m_id = row['id']
        method_nodes.add(m_id)
        has_method_edges.add((c_id, m_id))

# External
external_classes_created = set()
for row in external_method_batch:
    e_id = row['class_name']
    m_id = row['id']
    external_classes_created.add(e_id)
    method_nodes.add(m_id)
    has_method_edges.add((e_id, m_id))

print(f"Simulated Method Nodes: {len(method_nodes)}")
print(f"Simulated HAS_METHOD Edges: {len(has_method_edges)}")
