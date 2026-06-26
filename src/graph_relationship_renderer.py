def render_relationships(primary_full: dict) -> str:
    """
    Renders structured Knowledge Graph Relationships strictly from Neo4j graph data.
    Does not use the LLM to summarize or paraphrase.
    """
    if not primary_full:
        return ""
        
    rels = primary_full.get("relationships", {})
    if not rels:
        return ""
        
    # Map them to Display Names
    display_rels = {}
    
    if rels.get("inherits"): 
        display_rels["Inheritance"] = rels["inherits"]
    else:
        # User requested to explicitly show "None" for inheritance if empty
        display_rels["Inheritance"] = ["None"]
        
    if rels.get("inherited_by"): display_rels["Inherited By"] = rels["inherited_by"]
    if rels.get("owning_class"): display_rels["Owning Class"] = rels["owning_class"]
    
    # Add () to methods/functions
    if rels.get("methods"): display_rels["Methods"] = [f"{m}()" for m in rels["methods"]]
    if rels.get("returned_by"): display_rels["Returned By"] = [f"{m}()" for m in rels["returned_by"]]
    if rels.get("used_as_parameter"): display_rels["Used As Parameter"] = [f"{m}()" for m in rels["used_as_parameter"]]
    
    # Types and variables without ()
    if rels.get("returns"): display_rels["Returns"] = rels["returns"]
    if rels.get("parameters"): display_rels["Parameters"] = rels["parameters"]
    if rels.get("enum_values"): display_rels["Values"] = rels["enum_values"]
    if rels.get("calls"): display_rels["Calls"] = [f"{m}()" for m in rels["calls"]]
    if rels.get("called_by"): display_rels["Called By"] = [f"{m}()" for m in rels["called_by"]]
    
    lines = []
    lines.append("-" * 50)
    lines.append("")
    lines.append("Knowledge Graph Relationships")
    lines.append("")
    
    # Order to display
    display_order = [
        "Inheritance", "Inherited By", "Owning Class",
        "Methods", "Returns", "Parameters", "Values",
        "Returned By", "Used As Parameter", "Calls", "Called By"
    ]
    
    has_any = False
    for key in display_order:
        if key in display_rels:
            items = display_rels[key]
            lines.append(key)
            lines.append("")
            for item in items:
                lines.append(f"• {item}")
            lines.append("")
            has_any = True
            
    # Format Depth-2 Call Graph Tree if present
    call_graph_tree = primary_full.get("call_graph_tree")
    if call_graph_tree:
        lines.append("-" * 50)
        lines.append("")
        lines.append("Call Graph (Depth 2)")
        lines.append("")
        lines.append(call_graph_tree)
        lines.append("")
        has_any = True

    if not has_any:
        return ""
        
    return "\n".join(lines)
