def format_response(graphrag_output: dict) -> str:
    query = graphrag_output.get("query", "")
    answer = graphrag_output.get("answer", "")
    sources = graphrag_output.get("sources", [])
    r_time = graphrag_output.get("retrieval_time")
    g_time = graphrag_output.get("generation_time")
    t_time = graphrag_output.get("total_time")
    
    # 1. Primary Entity Detection
    primary_entity = None
    lower_q = query.lower()
    
    # Detect from generic queries like "What is X?"
    if lower_q.startswith("what is ") or lower_q.startswith("who is "):
        clean_q = query[8:].strip("?")
        tokens = clean_q.split()
        if tokens:
            primary_candidate = tokens[0]
            for s in sources:
                if s.get("entity_name") == primary_candidate:
                    primary_entity = primary_candidate
                    break
    
    if not primary_entity:
        # Fallback keyword detection
        for s in sources:
            if s.get("entity_name") and s.get("entity_name").lower() in lower_q:
                primary_entity = s.get("entity_name")
                break

    # 2. Group and deduplicate sources
    grouped_related = {}
    supporting_refs = []
    
    # Keep track of deduplicated names globally
    seen_names = set()
    if primary_entity:
        seen_names.add(primary_entity)
        
    for s in sources:
        e_type = s.get("entity_type", "Entity")
        e_name = s.get("entity_name", "Unknown")
        
        if e_type == "Entity" or e_name == "Unknown":
            continue
            
        if e_type.endswith("s"):
            plural_type = e_type
        elif e_type == "Class":
            plural_type = "Classes"
        else:
            plural_type = e_type + "s"
            
        if e_name == primary_entity:
            continue
            
        if e_name not in seen_names:
            seen_names.add(e_name)
            if plural_type not in grouped_related:
                grouped_related[plural_type] = []
            grouped_related[plural_type].append(e_name)
            supporting_refs.append(e_name)
            
    # Sort groups
    for k in grouped_related:
        grouped_related[k].sort()
    supporting_refs.sort()

    # Formatting
    lines = []
    lines.append("==================================================")
    lines.append("        ACIS CODE ASSISTANT")
    lines.append("==================================================")
    lines.append("")
    lines.append("Query")
    lines.append("-----")
    lines.append("")
    lines.append(query)
    lines.append("")
    lines.append("Answer")
    lines.append("------")
    lines.append("")
    lines.append(answer)
    lines.append("")
    
    if grouped_related:
        lines.append("Related Entities")
        lines.append("----------------")
        lines.append("")
        for g_type in sorted(grouped_related.keys()):
            lines.append(g_type)
            for e_name in grouped_related[g_type]:
                lines.append(f"• {e_name}")
            lines.append("")
            
    lines.append("Sources")
    lines.append("-------")
    lines.append("")
    if primary_entity:
        lines.append("Primary Entity")
        lines.append(f"• {primary_entity}")
        lines.append("")
        
    if supporting_refs:
        lines.append("Supporting References")
        for e_name in supporting_refs:
            lines.append(f"• {e_name}")
        lines.append("")
        
    if r_time is not None and g_time is not None and t_time is not None:
        lines.append("Performance")
        lines.append("-----------")
        lines.append("")
        lines.append(f"Retrieval  : {r_time*1000:.0f} ms")
        lines.append(f"Generation : {g_time:.3f} s")
        lines.append(f"Total      : {t_time:.3f} s")
        lines.append("")
        
    lines.append("==================================================")
    
    return "\n".join(lines)
