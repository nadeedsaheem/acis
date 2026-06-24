import os
import json
from tree_sitter import Language, Parser
import tree_sitter_cpp

# ==================================================
# CONFIGURATION
# ==================================================

REPO_ROOT = r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS"

FILE_PATH = r"C:\Users\Dell\OneDrive\Desktop\step1\ACIS\ACIS\include\ablapi.hxx"

# ==================================================
# TREE-SITTER SETUP
# ==================================================

CPP_LANGUAGE = Language(tree_sitter_cpp.language())
parser = Parser(CPP_LANGUAGE)

# ==================================================
# READ FILE
# ==================================================

with open(FILE_PATH, "rb") as f:
    code = f.read()

tree = parser.parse(code)

# ==================================================
# STORAGE
# ==================================================

functions = set()
classes = set()
includes = set()

# ==================================================
# HELPERS
# ==================================================

def get_text(node):
    return code[node.start_byte:node.end_byte].decode(
        "utf-8", errors="ignore"
    )

# ==================================================
# AST WALKER
# ==================================================

def walk(node):

    # ----------------------------------------------
    # FUNCTIONS
    # ----------------------------------------------
    if node.type == "function_declarator":

        for child in node.children:

            if child.type == "identifier":

                function_name = get_text(child).strip()

                if function_name:
                    functions.add(function_name)

    # ----------------------------------------------
    # CLASSES
    # ----------------------------------------------
    if node.type == "class_specifier":

        for child in node.children:

            if child.type == "type_identifier":

                class_name = get_text(child).strip()

                if class_name:
                    classes.add(class_name)

    # ----------------------------------------------
    # INCLUDES
    # ----------------------------------------------
    if node.type == "preproc_include":

        include_text = get_text(node)

        if '"' in include_text:

            try:
                include_file = include_text.split('"')[1]
                includes.add(include_file)
            except IndexError:
                pass

    # Recurse
    for child in node.children:
        walk(child)

# Start traversal
walk(tree.root_node)

# ==================================================
# FILE METADATA
# ==================================================

relative_path = os.path.relpath(
    FILE_PATH,
    REPO_ROOT
).replace("\\", "/")

extension = os.path.splitext(FILE_PATH)[1].lower()

if extension in [".h", ".hpp", ".hxx"]:
    file_type = "header"
elif extension in [".cpp", ".cc", ".cxx", ".c"]:
    file_type = "source"
else:
    file_type = "unknown"

# ==================================================
# BUILD RESULT
# ==================================================

result = {
    "file": os.path.basename(FILE_PATH),
    "path": relative_path,
    "file_type": file_type,

    "stats": {
        "function_count": len(functions),
        "class_count": len(classes),
        "include_count": len(includes)
    },

    "functions": sorted(functions),
    "classes": sorted(classes),
    "includes": sorted(includes)
}

# ==================================================
# PRINT RESULT
# ==================================================

print(json.dumps(result, indent=2))

# ==================================================
# SAVE JSON
# ==================================================

output_file = os.path.splitext(
    os.path.basename(FILE_PATH)
)[0] + "_parsed.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f"\nJSON saved to: {output_file}")