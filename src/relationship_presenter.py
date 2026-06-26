import re

def extract_relationships(primary_entity: dict, all_results: list) -> dict:
    """
    Extracts relationships (Inheritance, Methods, Returns, Uses Types) 
    for the primary entity from the retrieved context (results list and documentation strings),
    without executing any new graph queries.
    """
    rels = {
        "Inheritance": [],
        "Methods": [],
        "Returns": [],
        "Uses Types": []
    }
    
    if not primary_entity:
        return rels
        
    p_name = primary_entity.get("name", "")
    p_type = primary_entity.get("entity_type", "Entity")
    
    # 1. Check for Inheritance in documentation
    doc = primary_entity.get("documentation", "")
    inherit_match = re.search(r'Inherits:\s*([A-Za-z0-9_:]+)', doc, re.IGNORECASE)
    if inherit_match:
        base_class = inherit_match.group(1).strip()
        rels["Inheritance"].append(f"{base_class} \u2193 {p_name}")
        
    # Also check if any retrieved class inherits from this class
    for r in all_results:
        if r.get("entity_type") in ["Class", "Struct"]:
            r_doc = r.get("documentation", "")
            r_inherit = re.search(r'Inherits:\s*([A-Za-z0-9_:]+)', r_doc, re.IGNORECASE)
            if r_inherit and r_inherit.group(1).strip() == p_name:
                child_name = r.get("name", "")
                rel_str = f"{p_name} \u2193 {child_name}"
                if rel_str not in rels["Inheritance"]:
                    rels["Inheritance"].append(rel_str)
                    
    # 2. Check for Methods
    if p_type in ["Class", "Struct"]:
        for r in all_results:
            if r.get("entity_type") == "Method" and r.get("parent_class") == p_name:
                m_name = f"{r.get('name')}()"
                if m_name not in rels["Methods"]:
                    rels["Methods"].append(m_name)
                    
    # 3. Check for Returns
    if p_type in ["Function", "Method"]:
        ret = primary_entity.get("return_type")
        if ret and ret != "void":
            rels["Returns"].append(ret)
            
    # Also check if other functions return this entity
    if p_type in ["Class", "Struct", "Typedef", "Enum"]:
        for r in all_results:
            if r.get("entity_type") in ["Function", "Method"]:
                if r.get("return_type") == p_name:
                    f_name = f"{r.get('name')}()"
                    if f_name not in rels["Returns"]:
                        rels["Returns"].append(f_name)
                        
    # 4. Check for Uses Types (Parameters)
    if p_type in ["Function", "Method"]:
        params = primary_entity.get("parameters", [])
        for p in params:
            t = p.get("type", "")
            # Clean type (remove pointers, const, etc)
            clean_t = t.replace("const", "").replace("*", "").replace("&", "").strip()
            if clean_t and clean_t not in rels["Uses Types"] and clean_t not in ["int", "double", "float", "char", "void", "bool"]:
                rels["Uses Types"].append(clean_t)
                
    # Also check if this entity is used as a parameter in retrieved functions
    if p_type in ["Class", "Struct", "Typedef", "Enum"]:
        for r in all_results:
            if r.get("entity_type") in ["Function", "Method"]:
                params = r.get("parameters", [])
                for p in params:
                    clean_t = p.get("type", "").replace("const", "").replace("*", "").replace("&", "").strip()
                    if clean_t == p_name:
                        f_name = f"{r.get('name')}()"
                        if f_name not in rels["Uses Types"]:
                            rels["Uses Types"].append(f_name)
                            
    # Clean up empty
    return {k: v for k, v in rels.items() if v}

def get_graph_statistics(primary_entity: dict, all_results: list) -> dict:
    """Returns basic counts of related components present in the retrieval."""
    stats = {}
    if not primary_entity: return stats
    
    p_name = primary_entity.get("name", "")
    
    methods = 0
    related_funcs = 0
    
    for r in all_results:
        if r.get("name") == p_name: continue
        
        if r.get("parent_class") == p_name:
            methods += 1
        elif r.get("entity_type") == "Function":
            related_funcs += 1
            
    if methods > 0:
        stats["Methods"] = methods
    if related_funcs > 0:
        stats["Related Functions"] = related_funcs
        
    return stats
