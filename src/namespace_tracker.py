import re

def clean_type_name(name):
    if not name:
        return ""
    # Strip comments and template parameters
    name = re.sub(r'//.*', '', name)
    name = re.sub(r'/\*.*?\*/', '', name, flags=re.DOTALL)
    name = name.replace("class ", "").replace("struct ", "").replace("typename ", "").strip()
    if "<" in name:
        name = name.split("<")[0].strip()
    return name

def get_scope_stack(node, text_func):
    """
    Traverse tree-sitter AST nodes upwards from current node to root.
    Returns:
        namespaces (list): Namespaces from outermost to innermost (e.g., ["acis", "topology"])
        classes (list): Class/struct scopes from outermost to innermost (e.g., ["BODY", "Inner"])
    """
    namespaces = []
    classes = []
    
    curr = node.parent
    while curr:
        if curr.type in ("class_specifier", "struct_specifier"):
            name_node = curr.child_by_field_name("name")
            if name_node:
                cls_name = text_func(name_node).strip()
                cls_name_clean = clean_type_name(cls_name)
                if cls_name_clean:
                    classes.append(cls_name_clean)
        elif curr.type == "namespace_definition":
            ns_name = None
            for child in curr.children:
                if child.type in ("identifier", "namespace_identifier"):
                    ns_name = text_func(child).strip()
                    break
            if ns_name:
                ns_parts = [p.strip() for p in ns_name.split("::") if p.strip()]
                namespaces.extend(reversed(ns_parts))
        curr = curr.parent

    namespaces.reverse()
    classes.reverse()
    return namespaces, classes

def resolve_fqn(name, lexical_namespaces, lexical_classes, explicit_owner=None):
    """
    Resolve and construct the FQN of an entity by merging lexical context and explicit scope.
    """
    name_clean = clean_type_name(name)
    if not name_clean:
        return ""

    # Merge explicit owner (like BODY::method or acis::topology::BODY::method)
    namespaces = list(lexical_namespaces)
    classes = list(lexical_classes)
    
    if explicit_owner:
        owner_clean = clean_type_name(explicit_owner)
        owner_parts = [p.strip() for p in owner_clean.split("::") if p.strip()]
        
        # Determine how much of owner_parts belongs to namespace vs class
        # For simplicity, if lexical_classes is not empty, and owner_parts matches classes, merge them.
        # Generally, owner_parts are classes unless qualified with namespaces.
        # Let's align owner_parts: if the first part matches lexical_namespaces, it's namespace-qualified.
        # Otherwise, treat owner_parts as enclosing classes.
        for part in owner_parts:
            if part in namespaces:
                continue
            # If it's a known namespace, or just class
            # Since C++ names are resolved, we just append to classes unless it is a namespace qualifier.
            # But wait, if explicit_owner contains namespaces (e.g. acis::BODY), we should place acis in namespaces.
            # A simple rule: if part is lowercase or starts with acis or std, treat as namespace, otherwise class.
            # Alternatively, if classes is empty and namespaces has a prefix, keep it clean.
            # Let's do: if it's already in lexical context, ignore duplicate.
            # If not, let's append it to classes.
            if part not in classes:
                classes.append(part)
                
    # Construct FQN
    fqn_parts = namespaces + classes + [name_clean]
    return "::".join(fqn_parts)
