import json

with open('code_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

classes = set()
methods = set()
bases = set()

for item in data:
    for c in item.get('classes', []):
        if c.get('name'): classes.add(c.get('name'))
    for m in item.get('methods', []):
        if m.get('class'): methods.add(m.get('class'))
    for inh in item.get('inheritance', []):
        if inh.get('base'): bases.add(inh.get('base'))

print("Classes with < or ::")
print([c for c in classes if '<' in c or '::' in c])
print("Methods with < or ::")
print([m for m in methods if '<' in m or '::' in m])
print("Bases with < or ::")
print([b for b in bases if '<' in b or '::' in b])
