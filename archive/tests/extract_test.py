from tree_sitter import Language, Parser
import tree_sitter_cpp

CPP_LANGUAGE = Language(tree_sitter_cpp.language())

parser = Parser(CPP_LANGUAGE)

with open(r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS\include\ablapi.hxx", "rb") as f:
    code = f.read()

tree = parser.parse(code)

root = tree.root_node

def walk(node):
    print(node.type)

    for child in node.children:
        walk(child)

walk(root)