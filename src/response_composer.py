import re
from graph_relationship_renderer import render_relationships
from graph_evidence_renderer import render_evidence

def compose_response(graphrag_output: dict) -> dict:
    """
    Composes the final response by merging the LLM's explanation with 
    the verbatim graph relationships and evidence sections.
    """
    query = graphrag_output.get("query", "")
    answer = graphrag_output.get("answer", "")
    sources = graphrag_output.get("sources", [])
    full_results = graphrag_output.get("full_results", [])
    
    primary_entity = None
    primary_entity_type = None
    primary_full = None
    
    if sources:
        primary_entity = sources[0].get("entity_name")
        primary_entity_type = sources[0].get("entity_type", "Entity")
        if full_results:
            primary_full = full_results[0]
            
    # Parse LLM Answer Sections
    sections = {}
    summary = None
    
    if "No relevant information was found" in answer:
        pass
    else:
        parts = re.split(r'^##\s+', answer, flags=re.MULTILINE)
        if len(parts) > 1:
            for part in parts[1:]:
                lines = part.split("\n", 1)
                heading = lines[0].strip()
                content = lines[1].strip() if len(lines) > 1 else ""
                key = heading.lower().replace(" ", "_")
                sections[key] = content
                if not summary:
                    summary = content
        else:
            summary = answer

    lines = []
    lines.append("==================================================")
    lines.append("            ACIS CODE ASSISTANT")
    lines.append("==================================================")
    lines.append("")
    lines.append("Query")
    lines.append("")
    lines.append(query)
    lines.append("")
    
    if "No relevant information was found" in answer or not sections:
        lines.append(answer)
        lines.append("")
    else:
        if primary_entity:
            lines.append("Primary Entity")
            lines.append("")
            primary_display = f"{primary_entity}()" if primary_entity_type in ["Function", "Method"] else primary_entity
            lines.append(f"{primary_display} ({primary_entity_type})")
            lines.append("")
            
        # LLM Explanation output
        for heading, content in sections.items():
            if not content.strip(): continue
            display_heading = heading.replace("_", " ").title()
            lines.append(display_heading)
            lines.append("")
            lines.append(content)
            lines.append("")
            
        # Append Structured Graph Relationships
        rel_block = render_relationships(primary_full)
        if rel_block:
            lines.append(rel_block)
            
        # Append Knowledge Graph Evidence
        ev_block = render_evidence(sources, primary_entity, primary_entity_type)
        if ev_block:
            lines.append(ev_block)
            
    lines.append("==================================================")
    
    formatted_answer = "\n".join(lines)
    
    graphrag_output["formatted_answer"] = formatted_answer
    graphrag_output["summary"] = summary
    graphrag_output["sections"] = sections
    
    return graphrag_output
