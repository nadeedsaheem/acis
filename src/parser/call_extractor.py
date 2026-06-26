import os
import logging
from parser.fqn_resolver import get_canonical_key

class CallExtractor:
    def __init__(self, fqn_resolver=None):
        self.fqn_resolver = fqn_resolver

    def extract_local_variables(self, function_node, code_text):
        """
        Extracts variable name -> type mapping from parameters and local declarations.
        """
        var_types = {}
        
        def text(n):
            return code_text[n.start_byte:n.end_byte].decode("utf-8", errors="ignore")
            
        # Helper to find identifiers recursively
        def find_identifiers(n, names_list):
            if n.type == "identifier":
                names_list.append(text(n).strip())
            for child in n.children:
                find_identifiers(child, names_list)

        def walk_for_decls(n):
            # Skip nested function definitions or class declarations inside lambdas/inline helper blocks
            if n != function_node and n.type in ("function_definition", "class_specifier", "struct_specifier"):
                return
                
            if n.type == "parameter_declaration":
                type_node = n.child_by_field_name("type")
                decl_node = n.child_by_field_name("declarator")
                if type_node and decl_node:
                    t_name = text(type_node).strip()
                    names = []
                    find_identifiers(decl_node, names)
                    for name in names:
                        var_types[name] = t_name
            elif n.type == "declaration":
                type_node = n.child_by_field_name("type")
                if type_node:
                    t_name = text(type_node).strip()
                    names = []
                    for child in n.children:
                        if child != type_node:
                            find_identifiers(child, names)
                    for name in names:
                        var_types[name] = t_name
                        
            for child in n.children:
                walk_for_decls(child)
                
        walk_for_decls(function_node)
        return var_types

    def extract_calls(self, function_node, code_text, caller_fqn, caller_class, caller_namespaces, caller_parents):
        """
        Walks the function definition to extract call_expressions and resolve their FQNs.
        """
        calls = []
        var_types = self.extract_local_variables(function_node, code_text)
        
        # If caller is a method, 'this' points to its class type
        if caller_class:
            var_types["this"] = caller_class.split("::")[-1]

        def text(n):
            return code_text[n.start_byte:n.end_byte].decode("utf-8", errors="ignore")

        def walk_for_calls(n):
            # Skip nested function definitions
            if n != function_node and n.type == "function_definition":
                return
                
            if n.type == "call_expression":
                func_node = n.child_by_field_name("function")
                if func_node:
                    callee_name = ""
                    callee_fqn = None
                    callee_kind = "direct"
                    
                    # 1. Template function support (e.g. foo<int>())
                    if func_node.type == "template_function":
                        name_child = func_node.child_by_field_name("name")
                        if name_child:
                            func_node = name_child
                            
                    # 2. Member function call: obj.foo() or obj->foo()
                    if func_node.type == "field_expression":
                        obj_node = func_node.child_by_field_name("argument")
                        field_node = func_node.child_by_field_name("field")
                        if obj_node and field_node:
                            obj_name = text(obj_node).strip()
                            callee_name = text(field_node).strip()
                            callee_kind = "member"
                            
                            # Resolve object type
                            obj_type = var_types.get(obj_name)
                            if obj_type:
                                if self.fqn_resolver:
                                    class_fqn = self.fqn_resolver.resolve_type_fqn(obj_type, caller_namespaces, caller_parents)
                                else:
                                    class_fqn = obj_type
                                callee_fqn = f"{class_fqn}::{callee_name}"
                            else:
                                # Static method or uppercase name match
                                if obj_name[0].isupper() if obj_name else False:
                                    if self.fqn_resolver:
                                        class_fqn = self.fqn_resolver.resolve_type_fqn(obj_name, caller_namespaces, caller_parents)
                                    else:
                                        class_fqn = obj_name
                                    callee_fqn = f"{class_fqn}::{callee_name}"
                                else:
                                    callee_fqn = f"unresolved::{obj_name}::{callee_name}"
                                    
                    # 3. Qualified call: ns::foo() or Class::foo()
                    elif func_node.type == "qualified_identifier":
                        scope_node = func_node.child_by_field_name("scope")
                        name_node = func_node.child_by_field_name("name")
                        if scope_node and name_node:
                            scope_name = text(scope_node).strip()
                            callee_name = text(name_node).strip()
                            callee_kind = "qualified"
                            
                            if self.fqn_resolver:
                                scope_fqn = self.fqn_resolver.resolve_type_fqn(scope_name, caller_namespaces, caller_parents)
                            else:
                                scope_fqn = scope_name
                            callee_fqn = f"{scope_fqn}::{callee_name}"
                            
                    # 4. Direct call: foo()
                    elif func_node.type == "identifier":
                        callee_name = text(func_node).strip()
                        callee_kind = "direct"
                        
                        # Heuristics:
                        # a. Is it a method on caller_class?
                        # b. Or in current namespace scope?
                        if caller_class:
                            callee_fqn = f"{caller_class}::{callee_name}"
                        else:
                            scope_str = "::".join(caller_namespaces)
                            if scope_str:
                                callee_fqn = f"{scope_str}::{callee_name}"
                            else:
                                callee_fqn = callee_name
                                
                    if callee_name:
                        calls.append({
                            "caller": caller_fqn,
                            "callee_name": callee_name,
                            "callee_fqn": callee_fqn or f"unresolved::{callee_name}",
                            "kind": callee_kind,
                            "line": n.start_point[0] + 1
                        })
                        
            for child in n.children:
                walk_for_calls(child)
                
        walk_for_calls(function_node)
        return calls
