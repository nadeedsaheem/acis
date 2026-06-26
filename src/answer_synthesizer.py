def classify_question(query: str) -> str:
    lower_q = query.lower()
    
    if "where" in lower_q or "file" in lower_q:
        return "Navigation"
    elif "which" in lower_q or "inherit" in lower_q or "belong" in lower_q or "return" in lower_q:
        return "Relationship"
    elif "how" in lower_q or "work" in lower_q or "operate" in lower_q or "track" in lower_q:
        return "Functional Explanation"
    else:
        return "Definition"

def build_synthesis_prompt(query: str, context: str) -> tuple:
    category = classify_question(query)
    
    system_prompt = """You are a professional ACIS C++ Engineering Assistant.
Answer strictly from the supplied graph context. Do not invent APIs or classes.
If no grounded evidence exists, respond EXACTLY with:
"No relevant information was found in the current knowledge graph.

Suggestions

• Verify the symbol spelling.
• Try a broader technical description.
• Search for a related class or function."
"""

    if category == "Definition":
        layout = "## Definition\n## Purpose\n## Key Responsibilities\n## Common Usage\n## Related Components"
        target_len = "100-150 words"
    elif category == "Functional Explanation":
        layout = "## Summary\n## Workflow\n## Key Functions\n## Key Classes\n## Technical Notes"
        target_len = "200-350 words"
    elif category == "Relationship":
        layout = "## Summary\n## Matching Entities\n## Relationships"
        target_len = "5-15 entities maximum"
    else:
        layout = "## Answer\n## Relevant Files\n## Related Components"
        target_len = "100-150 words"

    user_prompt = f"""[GRAPH CONTEXT]
{context}

[QUESTION]
{query}

[INSTRUCTIONS]
Category: {category}
Layout required:
{layout}

Synthesize the documentation deeply using the graph relationships.
Target length: {target_len}.
Never use generic filler like "It is important for geometry."
Every sentence must be grounded in retrieved documentation.
"""
    return system_prompt, user_prompt, category
