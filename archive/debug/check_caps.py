import json

with open("all_entities.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

caps_functions = []
caps_methods = []

for item in dataset:
    for fn in item.get("functions", []):
        name = fn["name"]
        if name.isupper() and len(name) > 1:
            caps_functions.append((name, item["path"]))
    for m in item.get("methods", []):
        name = m["name"]
        if name.isupper() and len(name) > 1:
            caps_methods.append((name, item["path"]))

print(f"Found {len(caps_functions)} all-caps functions:")
for name, path in caps_functions[:30]:
    print(f"  - {name} ({path})")

print(f"\nFound {len(caps_methods)} all-caps methods:")
for name, path in caps_methods[:30]:
    print(f"  - {name} ({path})")
