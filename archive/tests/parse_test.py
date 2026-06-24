from tree_sitter import Language, Parser
import tree_sitter_cpp

print("Starting...")

CPP_LANGUAGE = Language(tree_sitter_cpp.language())

parser = Parser(CPP_LANGUAGE)

with open(r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS\include\ablapi.hxx", "rb") as f:
    code = f.read()
tree = parser.parse(code)

print("Parsed successfully!")
print(tree.root_node)