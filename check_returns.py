import json

def check():
    with open('code_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    no_ret_count = 0
    constructors = 0
    others = []
    
    for item in data:
        for f in item.get('functions', []):
            if not f.get('return_type'):
                no_ret_count += 1
                others.append(f"Function: {f.get('name')}")
        for m in item.get('methods', []):
            if not m.get('return_type'):
                no_ret_count += 1
                # Check if constructor
                if m.get('name') == m.get('class') or m.get('name') == '~' + m.get('class'):
                    constructors += 1
                else:
                    others.append(f"Method: {m.get('class')}::{m.get('name')}")
                    
    print(f"Total without return type: {no_ret_count}")
    print(f"Constructors/Destructors: {constructors}")
    print(f"Others: {len(others)}")
    for o in others[:10]:
        print(o)

check()
