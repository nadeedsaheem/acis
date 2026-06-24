import json

def test_docs():
    try:
        with open('code_base.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("code_base.json not found. Run multi_repo.py first.")
        return

    doc_funcs = 0
    doc_classes = 0
    total_funcs = 0
    total_classes = 0

    target_func = "api_set_abh_blends"
    target_func_doc = None

    for file_data in data:
        for f in file_data.get('functions', []):
            total_funcs += 1
            if f.get('documentation'):
                doc_funcs += 1
                if f['name'] == target_func and target_func_doc is None:
                    target_func_doc = f['documentation']
        
        for m in file_data.get('methods', []):
            total_funcs += 1
            if m.get('documentation'):
                doc_funcs += 1
                
        for c in file_data.get('classes', []):
            total_classes += 1
            if c.get('documentation'):
                doc_classes += 1

    print("========================================")
    print("DOCUMENTATION EXTRACTION VALIDATION")
    print("========================================")
    print(f"Total Functions/Methods: {total_funcs}")
    print(f"Functions/Methods with docs: {doc_funcs} ({(doc_funcs/total_funcs*100):.1f}%)" if total_funcs else "No functions found")
    print(f"Total Classes: {total_classes}")
    print(f"Classes with docs: {doc_classes} ({(doc_classes/total_classes*100):.1f}%)" if total_classes else "No classes found")
    print("----------------------------------------")
    if target_func_doc:
        print(f"Target function '{target_func}' doc:")
        print(f"-> {target_func_doc}")
    else:
        print(f"Target function '{target_func}' or its documentation not found.")
    print("========================================")

if __name__ == "__main__":
    test_docs()
