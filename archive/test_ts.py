import tree_sitter_cpp
from tree_sitter import Language, Parser

code = b"""
/*
 Creates advanced edge blends
*/
outcome api_set_abh_blends();

// ==========================
// Copyright (c) 2023
// ==========================

class MyClass {
    /// This is a method
    void do_something();
};
"""

CPP_LANGUAGE = Language(tree_sitter_cpp.language())
parser = Parser(CPP_LANGUAGE)
tree = parser.parse(code)

def walk(n):
    if n.type == 'comment':
        print(f"Comment: {n.start_point[0]+1}-{n.end_point[0]+1} {code[n.start_byte:n.end_byte]}")
    for c in n.children:
        walk(c)
walk(tree.root_node)
