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

internal_methods = set()
external_methods = set()

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
            
            if class_name in name_to_id:
                internal_methods.add(method_id)
            else:
                external_methods.add(method_id)

print(f"Internal Methods: {len(internal_methods)}")
print(f"External Methods: {len(external_methods)}")
