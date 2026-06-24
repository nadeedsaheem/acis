from tree_sitter import Language, Parser
import tree_sitter_cpp

CPP_LANGUAGE = Language(tree_sitter_cpp.language())
parser = Parser(CPP_LANGUAGE)

with open(r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS\include\ablapi.hxx", "rb") as f:
    code = f.read()

tree = parser.parse(code)

def walk(node):
    if node.type == "function_declarator":
        print("\nFOUND FUNCTION DECLARATOR:")
        print(code[node.start_byte:node.end_byte].decode("utf8"))

    for child in node.children:
        walk(child)

walk(tree.root_node)