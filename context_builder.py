def build_context(results: list, max_chars: int = 12000) -> str:
    """
    Generate clean structured markdown context from retrieval results.
    Prevents prompt overflow by truncating if max_chars is exceeded.
    """
    context_str = ""
    
    # Priority order if we need to truncate
    priority = {'Function': 1, 'Method': 2, 'Class': 3, 'Enum': 4, 'Struct': 5}
    
    # Sort results by score and priority
    sorted_results = sorted(results, key=lambda x: (x.get('score', 0), -priority.get(x.get('entity_type', ''), 99)), reverse=True)
    
    for r in sorted_results[:10]: # Maximum top 10 entities
        entity_type = r.get('entity_type', 'Entity')
        name = r.get('name') or r.get('entity_name') or 'Unknown'
        doc = r.get('documentation', '')
        ctx = r.get('context', {})
        
        block = f"## {entity_type}\n{name}\n\n"
        
        if doc:
            block += f"Documentation:\n{doc}\n\n"
            
        if entity_type in ['Function', 'Method']:
            if ctx.get('parent_class'):
                block += f"Parent Class: {ctx['parent_class']}\n\n"
            if ctx.get('parameters'):
                block += "Parameters:\n"
                for p in ctx['parameters']:
                    p_type = p.get('type', '')
                    p_name = p.get('name', '')
                    block += f"- {p_type} {p_name}\n"
                block += "\n"
            if ctx.get('return_type'):
                block += f"Returns:\n{ctx['return_type']}\n\n"
                
        elif entity_type == 'Class':
            parents = ctx.get('parents', [])
            if parents:
                block += "Inherits:\n" + ", ".join(parents) + "\n\n"
            methods = ctx.get('methods', [])
            if methods:
                block += "Methods:\n" + ", ".join(methods[:10]) + ("..." if len(methods)>10 else "") + "\n\n"
                
        elif entity_type == 'Enum':
            values = r.get('values', [])
            if values:
                block += "Values:\n" + ", ".join(values) + "\n\n"
                
        if len(context_str) + len(block) > max_chars:
            break
            
        context_str += block
        
    return context_str.strip()
