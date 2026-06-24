import json

def generate_report():
    try:
        with open('code_base.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("code_base.json not found.")
        return

    doc_funcs = 0
    doc_classes = 0
    total_funcs = 0
    total_classes = 0
    total_doc_length = 0
    total_doc_entities = 0

    target_func = "api_set_abh_blends"
    target_func_doc = None

    for file_data in data:
        for f in file_data.get('functions', []):
            total_funcs += 1
            if f.get('documentation'):
                doc_funcs += 1
                total_doc_length += len(f['documentation'])
                total_doc_entities += 1
                if f['name'] == target_func and target_func_doc is None:
                    target_func_doc = f['documentation']
        
        for m in file_data.get('methods', []):
            total_funcs += 1
            if m.get('documentation'):
                doc_funcs += 1
                total_doc_length += len(m['documentation'])
                total_doc_entities += 1
                
        for c in file_data.get('classes', []):
            total_classes += 1
            if c.get('documentation'):
                doc_classes += 1
                total_doc_length += len(c['documentation'])
                total_doc_entities += 1

    avg_length = total_doc_length / total_doc_entities if total_doc_entities else 0

    print("========================================")
    print("DOCUMENTATION CLEANING REPORT")
    print("========================================")
    print(f"Total Functions/Methods: {total_funcs}")
    print(f"Functions/Methods with docs: {doc_funcs} ({(doc_funcs/total_funcs*100):.1f}%)" if total_funcs else "No functions found")
    print(f"Total Classes: {total_classes}")
    print(f"Classes with docs: {doc_classes} ({(doc_classes/total_classes*100):.1f}%)" if total_classes else "No classes found")
    print(f"Average Documentation Length: {avg_length:.1f} characters")
    print("----------------------------------------")
    print("Example After Cleaning (api_set_abh_blends):")
    print(target_func_doc)
    print("========================================")

if __name__ == "__main__":
    generate_report()
