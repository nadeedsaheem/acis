def render_evidence(sources: list, primary_entity: str, primary_entity_type: str) -> str:
    """
    Renders structured Knowledge Graph Evidence.
    """
    if not sources:
        return ""
        
    seen_names = set()
    grouped_sources = {}
    
    if primary_entity:
        seen_names.add(primary_entity)
        
    for s in sources:
        e_type = s.get("entity_type", "Entity")
        e_name = s.get("entity_name", "Unknown")
        
        if e_type == "Entity" or e_name == "Unknown": continue
        if e_name == primary_entity: continue
            
        if e_name not in seen_names:
            seen_names.add(e_name)
            
            # Use appropriate pluralization
            if e_type == "Class":
                plural_type = "Classes"
            elif e_type.endswith("s"):
                plural_type = e_type
            else:
                plural_type = e_type + "s"
                
            if plural_type not in grouped_sources:
                grouped_sources[plural_type] = []
            grouped_sources[plural_type].append(e_name)
            
    lines = []
    lines.append("-" * 50)
    lines.append("")
    lines.append("Knowledge Graph Evidence")
    lines.append("")
    
    if primary_entity:
        lines.append("Primary Match")
        lines.append("")
        primary_display = f"{primary_entity}()" if primary_entity_type in ["Function", "Method"] else primary_entity
        lines.append(f"{primary_display}")
        lines.append("")
        
    if grouped_sources:
        for g_type, items in grouped_sources.items():
            lines.append(f"Supporting {g_type}")
            lines.append("")
            for e_name in items:
                display_name = f"{e_name}()" if g_type in ["Functions", "Methods"] else e_name
                lines.append(display_name)
            lines.append("")
            
    return "\n".join(lines)
