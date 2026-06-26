import re

def render_response(graphrag_output: dict) -> dict:
    query = graphrag_output.get("query", "")
    answer = graphrag_output.get("answer", "")
    sources = graphrag_output.get("sources", [])
    
    # 1. Primary Entity Detection
    primary_entity = None
    primary_entity_type = None
    lower_q = query.lower()
    
    if lower_q.startswith("what is ") or lower_q.startswith("who is "):
        clean_q = query[8:].strip("?")
        tokens = clean_q.split()
        if tokens:
            primary_candidate = tokens[0]
            for s in sources:
                if s.get("entity_name") == primary_candidate:
                    primary_entity = primary_candidate
                    primary_entity_type = s.get("entity_type", "Entity")
                    break
                    
    if not primary_entity:
        for s in sources:
            if s.get("entity_name") and s.get("entity_name").lower() in lower_q:
                primary_entity = s.get("entity_name")
                primary_entity_type = s.get("entity_type", "Entity")
                break

    # 2. Group and Deduplicate Sources
    seen_names = set()
    grouped_sources = {}
    
    if primary_entity:
        seen_names.add(primary_entity)
        
    for s in sources:
        e_type = s.get("entity_type", "Entity")
        e_name = s.get("entity_name", "Unknown")
        
        if e_type == "Entity" or e_name == "Unknown": continue
        
        # Pluralize
        if e_type == "Class":
            plural_type = "Classes"
        elif e_type.endswith("s"):
            plural_type = e_type
        else:
            plural_type = e_type + "s"
            
        if e_name == primary_entity:
            continue
            
        if e_name not in seen_names:
            seen_names.add(e_name)
            if plural_type not in grouped_sources:
                grouped_sources[plural_type] = []
            grouped_sources[plural_type].append(e_name)
            
    # Preserve retrieval ranking: do not sort alphabetically
    # Just maintain the order they were added to the list.

    # 3. Parse Sections from Answer
    sections = {}
    summary = None
    
    # If the answer is the hallucination fallback, don't parse sections
    if "No relevant information was found" in answer:
        pass
    else:
        # Split by ## Heading
        parts = re.split(r'^##\s+', answer, flags=re.MULTILINE)
        if len(parts) > 1:
            for part in parts[1:]:
                lines = part.split("\n", 1)
                heading = lines[0].strip()
                content = lines[1].strip() if len(lines) > 1 else ""
                key = heading.lower().replace(" ", "_")
                sections[key] = content
                
                if heading.lower() in ["summary", "definition", "answer"]:
                    if not summary:
                        summary = content
        else:
            summary = answer

    # 4. Render Formatted Output
    lines = []
    lines.append("==================================================")
    lines.append("          ACIS CODE ASSISTANT")
    lines.append("==================================================")
    lines.append("")
    lines.append("Query")
    lines.append("-----")
    lines.append("")
    lines.append(query)
    lines.append("")
    
    if "No relevant information was found" in answer or not sections:
        lines.append("Answer")
        lines.append("------")
        lines.append("")
        lines.append(answer)
        lines.append("")
    else:
        # In python dicts >= 3.7 insertion order is preserved, so we maintain original LLM order
        for heading, content in sections.items():
            display_heading = heading.replace("_", " ").title()
            if display_heading.lower() == "how it works": display_heading = "How It Works"
            lines.append(display_heading)
            lines.append("-" * len(display_heading))
            lines.append("")
            lines.append(content)
            lines.append("")
            
    lines.append("Knowledge Graph Evidence")
    lines.append("------------------------")
    lines.append("")
    if primary_entity:
        lines.append("Primary Entity")
        lines.append("")
        lines.append(f"{primary_entity_type}")
        lines.append("")
        primary_display = f"{primary_entity}()" if primary_entity_type in ["Function", "Method"] else primary_entity
        lines.append(primary_display)
        lines.append("")
        
    if grouped_sources:
        for g_type, items in grouped_sources.items():
            lines.append(f"Related {g_type}")
            lines.append("")
            for e_name in items:
                display_name = f"{e_name}()" if g_type in ["Functions", "Methods"] else e_name
                lines.append(display_name)
                lines.append("")
            
    lines.append("==================================================")
    formatted_answer = "\n".join(lines)
    
    graphrag_output["formatted_answer"] = formatted_answer
    graphrag_output["summary"] = summary
    graphrag_output["sections"] = sections
    
    return graphrag_output
