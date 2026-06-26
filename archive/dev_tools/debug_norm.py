import json
import hashlib

def normalize_class_name(name):
    if not name: return name
    name = name.split('<')[0]
    if '::' in name:
        name = name.split('::')[-1]
    name = name.replace('class ', '').replace('struct ', '').strip()
    return name

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

orphan_methods = []
for item in data:
    path = item.get('path')
    if not path: continue
    for md in item.get('methods', []):
        class_name = md.get('class')
        if class_name:
            norm_class_name = normalize_class_name(class_name)
            if norm_class_name not in name_to_id:
                orphan_methods.append((class_name, norm_class_name))

print(f"Orphan methods: {len(orphan_methods)}")
import collections
print("Sample orphans:", collections.Counter([x[1] for x in orphan_methods]).most_common(20))
