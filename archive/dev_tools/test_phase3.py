import json
import hashlib
import time
import re

def generate_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def normalize_class_name(name):
    if not name: return name
    name = name.split('<')[0]
    if '::' in name:
        name = name.split('::')[-1]
    name = name.replace('class ', '').replace('struct ', '').strip()
    return name

def normalize_parameter_type(type_str):
    if not type_str: return ""
    t = type_str
    t = t.replace('const ', '').replace(' const', '')
    t = t.replace('class ', '').replace('struct ', '').replace('typename ', '')
    t = t.replace('*', '').replace('&', '')
    t = t.strip()
    return t

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
            norm_name = normalize_class_name(name)
            if norm_name not in name_to_id:
                name_to_id[norm_name] = class_id

params_parsed = 0
params_loaded = 0
param_ids = set()
duplicate_param_ids = 0
uses_type_count = 0
unresolved_types = 0

for item in data:
    path = item.get('path')
    if not path: continue
    
    # Functions
    for fn in item.get('functions', []):
        name = fn.get('name')
        if name:
            params = fn.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            signature = f"{name}({param_str})"
            line_number = fn.get('line_number', 0)
            raw_id = f"{path}::{name}::{signature}::{line_number}"
            func_id = generate_hash(raw_id)
            
            for pos, p in enumerate(params):
                params_parsed += 1
                p_name = p.get('name', '')
                p_type = p.get('type', '')
                raw_p_id = f"{func_id}::param::{pos}::{p_name}::{p_type}"
                p_id = generate_hash(raw_p_id)
                
                if p_id in param_ids:
                    duplicate_param_ids += 1
                else:
                    param_ids.add(p_id)
                    params_loaded += 1
                    norm_type = normalize_parameter_type(p_type)
                    # Resolve uses_type
                    if norm_type in name_to_id:
                        uses_type_count += 1
                    else:
                        unresolved_types += 1

    # Methods
    for md in item.get('methods', []):
        name = md.get('name')
        class_name = md.get('class')
        if name and class_name:
            params = md.get('parameters', [])
            param_str = ", ".join(p.get('type', '') for p in params)
            signature = f"{name}({param_str})"
            line_number = md.get('line_number', 0)
            
            raw_id = f"{path}::{name}::{signature}::{line_number}"
            method_id = generate_hash(raw_id)
            
            for pos, p in enumerate(params):
                params_parsed += 1
                p_name = p.get('name', '')
                p_type = p.get('type', '')
                raw_p_id = f"{method_id}::param::{pos}::{p_name}::{p_type}"
                p_id = generate_hash(raw_p_id)
                
                if p_id in param_ids:
                    duplicate_param_ids += 1
                else:
                    param_ids.add(p_id)
                    params_loaded += 1
                    norm_type = normalize_parameter_type(p_type)
                    # Resolve uses_type
                    if norm_type in name_to_id:
                        uses_type_count += 1
                    else:
                        unresolved_types += 1

print(f"Parsed: {params_parsed}")
print(f"Loaded: {params_loaded}")
print(f"Duplicates: {duplicate_param_ids}")
print(f"USES_TYPE: {uses_type_count}")
print(f"Unresolved: {unresolved_types}")
