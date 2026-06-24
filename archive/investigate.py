import json
import os
import random
from tree_sitter import Language, Parser
import tree_sitter_cpp

REPO_ROOT = r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS"
CPP_LANGUAGE = Language(tree_sitter_cpp.language())
parser = Parser(CPP_LANGUAGE)

def text(node, code):
    return code[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")

def extract_entities(code):
    tree = parser.parse(code)
    
    classes = set()
    structs = set()
    typedefs = set()
    inheritance = set()
    
    # We will use queries or simple traversal
    def walk(n):
        if n.type == "class_specifier":
            name_node = n.child_by_field_name("name")
            if name_node:
                cname = text(name_node, code).strip()
                if cname: classes.add(cname)
                
                # Check base classes
                # Tree-sitter CPP class_specifier structure:
                # class_specifier [ name: (type_identifier) body: (class_body) ]
                # If there's inheritance, it uses a base_class_clause
                for child in n.children:
                    if child.type == "base_class_clause":
                        for sub in child.children:
                            if sub.type in ("type_identifier", "template_type", "identifier"):
                                base_name = text(sub, code).split("<")[0].strip()
                                inheritance.add((cname, base_name))
                            elif sub.type == "ERROR":
                                pass
        elif n.type == "struct_specifier":
            name_node = n.child_by_field_name("name")
            if name_node:
                sname = text(name_node, code).strip()
                if sname: structs.add(sname)
        elif n.type == "type_definition":
            decl = n.child_by_field_name("declarator")
            if decl:
                def get_alias(node):
                    if node.type in ("type_identifier", "identifier"): return text(node, code)
                    for c in node.children:
                        res = get_alias(c)
                        if res: return res
                    return None
                alias = get_alias(decl)
                if alias: typedefs.add(alias)
                
        # Handle MASTER_ATTRIB_DECL / MASTER_ENTITY_DECL macros
        if n.type == "call_expression":
            fn = n.child_by_field_name("function")
            if fn and text(fn, code) in ("MASTER_ATTRIB_DECL", "MASTER_ENTITY_DECL"):
                args = n.child_by_field_name("arguments")
                if args:
                    for arg in args.children:
                        if arg.type not in ("(", ")", ","):
                            cname = text(arg, code).strip()
                            classes.add(cname)
                            if text(fn, code) == "MASTER_ATTRIB_DECL":
                                inheritance.add((cname, "ATTRIB"))
                            else:
                                inheritance.add((cname, "ENTITY"))
                            break

        for child in n.children:
            walk(child)
            
    walk(tree.root_node)
    
    return classes, structs, typedefs, inheritance

def main():
    print("Loading data...")
    with open("verification_report.json", "r") as f:
        vr = json.load(f)
    with open("code_base.json", "r", encoding="utf-8") as f:
        cb = json.load(f)
        
    cb_dict = {item["path"]: item for item in cb}
    
    # 1. Investigate FP classes
    fps = vr.get("sampling_results", [])
    investigation_results = []
    
    print("Investigating false positive classes...")
    for item in fps:
        if item["type"] == "class_fp":
            filepath = item["file"]
            full_path = os.path.join(REPO_ROOT, filepath)
            try:
                with open(full_path, "rb") as f:
                    code = f.read()
            except:
                continue
                
            classes, structs, typedefs, inheritance = extract_entities(code)
            
            for cls_name in item["items"]:
                actual_type = "unknown"
                if cls_name in classes: actual_type = "class"
                elif cls_name in structs: actual_type = "struct"
                elif cls_name in typedefs: actual_type = "typedef"
                
                # Check cb
                record = cb_dict.get(filepath, {})
                parser_output = "unknown"
                if any(c["name"] == cls_name for c in record.get("classes", [])):
                    parser_output = "class"
                elif any(s["name"] == cls_name for s in record.get("structs", [])):
                    parser_output = "struct"
                    
                correct_result = ""
                if actual_type == parser_output:
                    correct_result = "verification_bug"
                elif actual_type in ("struct", "typedef") and parser_output == "class":
                    correct_result = "parser_bug"
                else:
                    correct_result = "ground_truth_bug"
                    
                investigation_results.append({
                    "entity": cls_name,
                    "source_file": filepath,
                    "actual_source_type": actual_type,
                    "parser_output": parser_output,
                    "verification_classification": "false_positive",
                    "correct_result": correct_result
                })

    with open("fp_investigation.json", "w") as f:
        json.dump(investigation_results, f, indent=2)

    # 2. Inheritance Audit
    print("Auditing inheritance...")
    all_edges = []
    for item in cb:
        for inh in item.get("inheritance", []):
            all_edges.append((item["path"], inh["class"], inh["base"]))
            
    sample_edges = random.sample(all_edges, min(100, len(all_edges)))
    
    correct_edges = 0
    incorrect_edges = 0
    
    for path, c, b in sample_edges:
        full_path = os.path.join(REPO_ROOT, path)
        try:
            with open(full_path, "rb") as f:
                code = f.read()
        except:
            incorrect_edges += 1
            continue
            
        classes, structs, typedefs, inheritance = extract_entities(code)
        # Check if the edge exists in the independent extraction
        # Because we only extract simple names, we should do partial matching
        found = False
        for ext_c, ext_b in inheritance:
            if c == ext_c and (b in ext_b or ext_b in b):
                found = True
                break
        if found:
            correct_edges += 1
        else:
            incorrect_edges += 1
            
    print(f"Inheritance Audit: Correct: {correct_edges}, Incorrect: {incorrect_edges}")
    
    # Calculate overall class precision/recall using AST ground truth on 100 sample files
    sample_files = list({item["file"] for item in fps}) # use the same files from verification report or just 100 random
    if len(sample_files) < 100:
        sample_files = random.sample(list(cb_dict.keys()), 100)
        
    ast_class_tp = 0
    ast_class_fp = 0
    ast_class_fn = 0
    
    ast_inh_tp = 0
    ast_inh_fp = 0
    ast_inh_fn = 0
    
    for path in sample_files:
        full_path = os.path.join(REPO_ROOT, path)
        try:
            with open(full_path, "rb") as f:
                code = f.read()
        except:
            continue
            
        gt_classes, _, _, gt_inh = extract_entities(code)
        
        record = cb_dict.get(path, {})
        ds_classes = {c["name"] for c in record.get("classes", [])}
        ds_inh = {(i["class"], i["base"]) for i in record.get("inheritance", [])}
        
        ast_class_tp += len(gt_classes.intersection(ds_classes))
        ast_class_fp += len(ds_classes - gt_classes)
        ast_class_fn += len(gt_classes - ds_classes)
        
        # for inheritance, base names might have namespaces or template args, so exact match might be harsh.
        # Let's do exact match first.
        ast_inh_tp += len(gt_inh.intersection(ds_inh))
        ast_inh_fp += len(ds_inh - gt_inh)
        ast_inh_fn += len(gt_inh - ds_inh)

    class_prec = ast_class_tp / (ast_class_tp + ast_class_fp) if (ast_class_tp + ast_class_fp) else 0
    class_rec = ast_class_tp / (ast_class_tp + ast_class_fn) if (ast_class_tp + ast_class_fn) else 0
    
    inh_prec = ast_inh_tp / (ast_inh_tp + ast_inh_fp) if (ast_inh_tp + ast_inh_fp) else 0
    inh_rec = ast_inh_tp / (ast_inh_tp + ast_inh_fn) if (ast_inh_tp + ast_inh_fn) else 0
    
    print(f"AST Class Prec: {class_prec:.2%}, Recall: {class_rec:.2%}")
    print(f"AST Inh Prec: {inh_prec:.2%}, Recall: {inh_rec:.2%}")
    
    with open("ast_metrics.json", "w") as f:
        json.dump({
            "class_prec": class_prec,
            "class_rec": class_rec,
            "inh_prec": inh_prec,
            "inh_rec": inh_rec
        }, f, indent=2)

if __name__ == "__main__":
    main()
