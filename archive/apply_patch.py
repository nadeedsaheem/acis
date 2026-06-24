import sys

with open("multi_repo.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Change namespaces to dict
code = code.replace("namespaces = set()", "namespaces = {}")

# 2. Add line numbers to classes
code = code.replace(
    'classes[class_name] = {"name": class_name, "documentation": doc}',
    'classes[class_name] = {"name": class_name, "documentation": doc, "line_number": node.start_point[0] + 1}'
)

# 3. Add line numbers to MACRO classes
code = code.replace(
    'classes[class_name] = {"name": class_name, "documentation": doc}',
    'classes[class_name] = {"name": class_name, "documentation": doc, "line_number": node.start_point[0] + 1}' # Handled above if global replace
)

# 4. Add line numbers to structs
code = code.replace(
    'structs[s_name] = {"name": s_name, "documentation": doc}',
    'structs[s_name] = {"name": s_name, "documentation": doc, "line_number": node.start_point[0] + 1}'
)

# 5. Add line numbers and values to enums
old_enum = """        if node.type == "enum_specifier":
            for child in node.children:
                if child.type == "type_identifier":
                    e_name = text(child)
                    doc = get_closest_comment(node.start_point[0] + 1)
                    if e_name not in enums or not enums[e_name].get("documentation"):
                        enums[e_name] = {"name": e_name, "documentation": doc}"""

new_enum = """        if node.type == "enum_specifier":
            e_name = None
            e_values = []
            for child in node.children:
                if child.type == "type_identifier":
                    e_name = text(child)
                elif child.type == "enumerator_list":
                    for sub in child.children:
                        if sub.type == "enumerator":
                            name_node = sub.child_by_field_name("name")
                            if name_node:
                                e_values.append(text(name_node))
            if e_name:
                doc = get_closest_comment(node.start_point[0] + 1)
                if e_name not in enums or not enums[e_name].get("documentation"):
                    enums[e_name] = {"name": e_name, "documentation": doc, "line_number": node.start_point[0] + 1, "values": e_values}"""
code = code.replace(old_enum, new_enum)

# 6. Add line numbers to typedefs
code = code.replace(
    'typedefs[alias_name] = {"name": alias_name, "documentation": doc}',
    'typedefs[alias_name] = {"name": alias_name, "documentation": doc, "line_number": node.start_point[0] + 1}'
)

# 7. Add line numbers to namespaces
old_ns = """        if node.type == "namespace_definition":
            for child in node.children:
                if child.type in ("identifier", "namespace_identifier"):
                    namespaces.add(text(child))"""

new_ns = """        if node.type == "namespace_definition":
            for child in node.children:
                if child.type in ("identifier", "namespace_identifier"):
                    ns_name = text(child)
                    if ns_name not in namespaces:
                        namespaces[ns_name] = {"name": ns_name, "line_number": node.start_point[0] + 1}"""
code = code.replace(old_ns, new_ns)

# 8. Modify namespaces output format
code = code.replace(
    '"namespaces": [{"name": ns} for ns in sorted(namespaces)],',
    '"namespaces": sorted(list(namespaces.values()), key=lambda x: x["name"]),'
)

# 9. Modify parameters parsing
old_get_params = """    def get_parameters(node):
        params_node = node.child_by_field_name("parameters")
        if not params_node:
            for child in node.children:
                if child.type == "parameter_list":
                    params_node = child
                    break
        params_list = []
        if params_node:
            for child in params_node.children:
                if child.type in ("parameter_declaration", "optional_parameter_declaration", "variadic_parameter_declaration"):
                    params_list.append(text(child).strip())
        return params_list"""

new_get_params = """    def get_parameters(node):
        params_node = node.child_by_field_name("parameters")
        if not params_node:
            for child in node.children:
                if child.type == "parameter_list":
                    params_node = child
                    break
        params_list = []
        if params_node:
            for child in params_node.children:
                if child.type in ("parameter_declaration", "optional_parameter_declaration", "variadic_parameter_declaration"):
                    decl_node = child.child_by_field_name("declarator")
                    
                    def get_id(n):
                        if n.type in ("identifier", "type_identifier", "field_identifier"):
                            return text(n)
                        for c in n.children:
                            res = get_id(c)
                            if res: return res
                        return None
                        
                    name = get_id(decl_node) if decl_node else ""
                    full_text = text(child).strip()
                    if "=" in full_text:
                        full_text = full_text.split("=", 1)[0].strip()
                        
                    if name and name in full_text:
                        idx = full_text.rfind(name)
                        type_str = full_text[:idx].strip()
                        post = full_text[idx+len(name):].strip()
                        type_str = (type_str + " " + post).strip()
                        params_list.append({"type": type_str, "name": name})
                    else:
                        params_list.append({"type": full_text, "name": name})
        return params_list"""
code = code.replace(old_get_params, new_get_params)

with open("multi_repo.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Patch applied.")
