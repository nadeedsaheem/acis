import os
import json

def clean_dataset(input_file="code_base.json", output_file="code_base_clean.json"):
    """
    Reads the raw all_entities.json file, filters out all redundant fields,
    detects fields automatically, preserves line_number if present,
    and writes the cleaned dataset to all_entities_clean.json.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    print(f"Reading '{input_file}'...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Transforming records to final canonical schema...")
    cleaned_data = []

    for item in data:
        # 1. Transform classes and structs to lists of objects with 'name' key
        # Handle cases where they might be strings or objects
        classes_raw = item.get("classes", [])
        classes_clean = []
        for c in classes_raw:
            if isinstance(c, dict):
                classes_clean.append({"name": c.get("name", "")})
            else:
                classes_clean.append({"name": str(c)})

        structs_raw = item.get("structs", [])
        structs_clean = []
        for s in structs_raw:
            if isinstance(s, dict):
                structs_clean.append({"name": s.get("name", "")})
            else:
                structs_clean.append({"name": str(s)})

        # 2. Keep enums, typedefs, namespaces, includes as flat lists of strings
        enums_clean = [str(e.get("name", e)) if isinstance(e, dict) else str(e) for e in item.get("enums", [])]
        typedefs_clean = [str(t.get("name", t)) if isinstance(t, dict) else str(t) for t in item.get("typedefs", [])]
        namespaces_clean = [str(n.get("name", n)) if isinstance(n, dict) else str(n) for n in item.get("namespaces", [])]
        includes_clean = [str(i) for i in item.get("includes", [])]

        # 3. Process methods (detecting class owner field automatically)
        methods_clean = []
        for m in item.get("methods", []):
            # Detect class owner field (could be class_owner, class, owner, parent_class, etc.)
            class_owner = ""
            for k in ["class_owner", "class", "owner", "parent_class"]:
                if k in m:
                    class_owner = m[k]
                    break
            
            method_obj = {
                "class": class_owner or "",
                "name": m.get("name", ""),
                "return_type": m.get("return_type", ""),
                "parameters": m.get("parameters", [])
            }
            # Keep line number if present
            if "line_number" in m:
                method_obj["line_number"] = m["line_number"]
            
            methods_clean.append(method_obj)

        # 4. Process functions
        functions_clean = []
        for fn in item.get("functions", []):
            fn_obj = {
                "name": fn.get("name", ""),
                "return_type": fn.get("return_type", ""),
                "parameters": fn.get("parameters", [])
            }
            # Keep line number if present
            if "line_number" in fn:
                fn_obj["line_number"] = fn["line_number"]
                
            functions_clean.append(fn_obj)

        # 5. Process inheritance
        inheritance_clean = []
        for inh in item.get("inheritance", []):
            inheritance_clean.append({
                "class": inh.get("class", ""),
                "base": inh.get("base", "")
            })

        # Assemble final canonical object
        cleaned_item = {
            "file": item.get("file", ""),
            "path": item.get("path", ""),
            "classes": classes_clean,
            "structs": structs_clean,
            "enums": enums_clean,
            "typedefs": typedefs_clean,
            "namespaces": namespaces_clean,
            "includes": includes_clean,
            "methods": methods_clean,
            "functions": functions_clean,
            "inheritance": inheritance_clean
        }
        
        cleaned_data.append(cleaned_item)

    print(f"Writing cleaned data to '{output_file}'...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print("Done! Transformation complete.")

if __name__ == "__main__":
    clean_dataset()
