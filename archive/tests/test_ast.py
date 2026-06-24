from tree_sitter import Language, Parser
import tree_sitter_cpp

CPP_LANGUAGE = Language(tree_sitter_cpp.language())
parser = Parser(CPP_LANGUAGE)

code = b"""
void (*get_callback())(int);
"""

tree = parser.parse(code)

def get_declarator_info(decl_node):
    curr = decl_node
    is_pointer = False
    is_reference = False
    is_func_ptr_var = False
    while curr:
        if curr.type == "pointer_declarator":
            is_pointer = True
            is_func_ptr_var = True
            curr = curr.child_by_field_name("declarator")
        elif curr.type == "reference_declarator":
            is_reference = True
            is_func_ptr_var = True
            curr = curr.child_by_field_name("declarator")
        elif curr.type == "parenthesized_declarator":
            if len(curr.children) >= 3:
                curr = curr.children[1]
            else:
                curr = None
        else:
            break
    return curr, is_pointer, is_reference, is_func_ptr_var

def print_ast(node, depth=0):
    indent = "  " * depth
    text_val = code[node.start_byte:node.end_byte].decode('utf8', errors='ignore')
    print(f"{indent}{node.type}: {text_val.strip()}")
    for child in node.children:
        print_ast(child, depth + 1)

print_ast(tree.root_node)

def walk(node):
    if node.type == "function_declarator":
        decl = node.child_by_field_name('declarator')
        if decl:
            name_node, is_ptr, is_ref, is_func_ptr_var = get_declarator_info(decl)
            name = code[name_node.start_byte:name_node.end_byte].decode('utf8') if name_node else "None"
            print(f"Name: {name} | is_func_ptr_var: {is_func_ptr_var}")
    for child in node.children:
        walk(child)

walk(tree.root_node)
