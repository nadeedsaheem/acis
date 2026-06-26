def inject_primary_entity_lock(system_prompt: str, primary_entity_name: str) -> str:
    """
    Injects strict grounding constraints into the LLM system prompt.
    Ensures that the LLM focuses primarily on the given primary_entity_name.
    """
    if not primary_entity_name:
        return system_prompt
        
    lock_rules = f"""
PRIMARY ENTITY:
{primary_entity_name}

The first sentence of the answer MUST begin by describing the primary entity ({primary_entity_name}) itself.
The Definition section MUST describe {primary_entity_name}.

Do not define:
- parent classes
- inherited classes
- related classes
- supporting evidence

Inherited classes may only be discussed in inheritance sections.
Supporting entities may not replace the primary entity in the definition section.
"""
    
    return system_prompt + "\n" + lock_rules
