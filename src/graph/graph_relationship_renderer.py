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
        
    def limit_list(items):
        if not items: return []
        if len(items) <= 5: return items
        return items[:5] + [f"(+{len(items) - 5} more)"]
        
    # Map them to Display Names
    display_rels = {}
    
    if rels.get("inherits"): 
        display_rels["Inheritance"] = limit_list(rels["inherits"])
    else:
        display_rels["Inheritance"] = ["None"]
        
    if rels.get("inherited_by"): display_rels["Inherited By"] = limit_list(rels["inherited_by"])
    if rels.get("owning_class"): display_rels["Owning Class"] = limit_list(rels["owning_class"])
    
    # Ownership topologies (new from graph_context_enricher)
    if rels.get("topology"): display_rels["Topological Hierarchy"] = limit_list(rels["topology"])
    
    # Add () to methods/functions
    if rels.get("methods"): display_rels["Methods"] = limit_list([f"{m}()" for m in rels["methods"]])
    if rels.get("returned_by"): display_rels["Returned By"] = limit_list([f"{m}()" for m in rels["returned_by"]])
    if rels.get("used_as_parameter"): display_rels["Used As Parameter"] = limit_list([f"{m}()" for m in rels["used_as_parameter"]])
    
    # Types and variables without ()
    if rels.get("returns"): display_rels["Returns"] = limit_list(rels["returns"])
    if rels.get("parameters"): display_rels["Parameters"] = limit_list(rels["parameters"])
    if rels.get("enum_values"): display_rels["Values"] = limit_list(rels["enum_values"])
    if rels.get("calls"): display_rels["Calls"] = limit_list([f"{m}()" for m in rels["calls"]])
    if rels.get("called_by"): display_rels["Called By"] = limit_list([f"{m}()" for m in rels["called_by"]])
    
    lines = []
    lines.append("-" * 50)
    lines.append("")
    lines.append("Knowledge Graph Relationships")
    lines.append("")
    
    # Order to display
    display_order = [
        "Inheritance", "Inherited By", "Topological Hierarchy", "Owning Class",
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
