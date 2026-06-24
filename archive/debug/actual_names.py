from tree_sitter import Language, Parser
import tree_sitter_cpp

CPP_LANGUAGE = Language(tree_sitter_cpp.language())
parser = Parser(CPP_LANGUAGE)

with open(r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS\include\ablapi.hxx", "rb") as f:
    code = f.read()

tree = parser.parse(code)

classes = []
methods = []

def walk(node):
    # Class names
    if node.type == "type_identifier":
        text = code[node.start_byte:node.end_byte].decode("utf8")
        classes.append(text)

    # Method names
    if node.type == "field_identifier":
        text = code[node.start_byte:node.end_byte].decode("utf8")
        methods.append(text)

    for child in node.children:
        walk(child)

walk(tree.root_node)

print("Classes:", classes)
print("Methods:", methods)