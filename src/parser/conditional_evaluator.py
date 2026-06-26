def evaluate_condition(node, macro_registry, code):
    node_type = node.type
    
    def get_text(n):
        return code[n.start_byte:n.end_byte].decode("utf-8", errors="ignore").strip()

    if node_type == "preproc_defined":
        # Check children for identifier
        for child in node.children:
            if child.type == "identifier":
                return macro_registry.is_defined(get_text(child))
        return False
        
    elif node_type == "identifier":
        name = get_text(node)
        if macro_registry.is_defined(name):
            val = macro_registry.get_value(name)
            try:
                # Strip integer suffixes like U, L, LL, etc.
                val_clean = val.rstrip('uUlL')
                if val_clean.startswith("0x") or val_clean.startswith("0X"):
                    return int(val_clean, 16) != 0
                return int(val_clean) != 0
            except ValueError:
                return val not in ("", "0", "false", "FALSE")
        return False
        
    elif node_type == "number_literal":
        text = get_text(node).rstrip('uUlL')
        try:
            if text.startswith("0x") or text.startswith("0X"):
                return int(text, 16) != 0
            return int(text) != 0
        except ValueError:
            return False
            
    elif node_type == "parenthesized_expression":
        for child in node.children:
            if child.type not in ("(", ")"):
                return evaluate_condition(child, macro_registry, code)
        return False
        
    elif node_type == "unary_expression":
        operator = None
        operand = None
        for child in node.children:
            if child.type in ("!", "~", "-", "+"):
                operator = child.type
            else:
                operand = child
        if operator == "!":
            return not evaluate_condition(operand, macro_registry, code)
        elif operator == "~":
            val = evaluate_condition(operand, macro_registry, code)
            return ~int(val) if isinstance(val, int) else not val
        elif operator == "-":
            val = evaluate_condition(operand, macro_registry, code)
            return -int(val) if isinstance(val, int) else 0
        elif operator == "+":
            return evaluate_condition(operand, macro_registry, code)
        return False
        
    elif node_type == "binary_expression":
        left = node.children[0]
        op = get_text(node.children[1])
        right = node.children[2]
        
        lval = evaluate_condition(left, macro_registry, code)
        rval = evaluate_condition(right, macro_registry, code)
        
        # Convert types if possible for comparison
        if isinstance(lval, bool) and not isinstance(rval, bool):
            lval = int(lval)
        if isinstance(rval, bool) and not isinstance(lval, bool):
            rval = int(rval)
            
        if op == "&&":
            return bool(lval and rval)
        elif op == "||":
            return bool(lval or rval)
        elif op == "==":
            return lval == rval
        elif op == "!=":
            return lval != rval
        elif op == "<":
            return lval < rval
        elif op == ">":
            return lval > rval
        elif op == "<=":
            return lval <= rval
        elif op == ">=":
            return lval >= rval
        return False
        
    return False
