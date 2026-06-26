def build_context(enriched_primary: list, supporting_entities: list, max_chars: int = 12000) -> str:
    """
    Transforms a list of enriched primary entity and supporting entities into a unified Markdown context payload.
    """
    context_blocks = []
    
    if enriched_primary:
        er = enriched_primary[0]
        entity = er.get("entity", {})
        doc = er.get("documentation", "").strip()
        
        parts = []
        parts.append("Primary Entity")
        parts.append(entity.get('name', 'Unknown'))
        parts.append("Entity Type")
        parts.append(entity.get('type', 'Entity'))
        
        if doc:
            parts.append(f"\nDocumentation\n{doc}")
            
        context_blocks.append("\n".join(parts))
        
    if supporting_entities:
        sup_parts = ["Supporting Evidence"]
        for se in supporting_entities:
            name = se.get('name') or se.get('entity_name') or 'Unknown'
            if se.get('entity_type') in ['Function', 'Method']:
                sup_parts.append(f"{name}()")
            else:
                sup_parts.append(name)
        
        context_blocks.append("\n".join(sup_parts))
        
    return "\n\n--------------------------------------------------\n\n".join(context_blocks)
