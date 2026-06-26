from retrieval.intent_entity_ranker import detect_intent
from llm.primary_entity_guard import inject_primary_entity_lock

def build_synthesis_prompt(query: str, context: str, primary_entity_name: str = None, is_retry: bool = False) -> tuple:
    intent = detect_intent(query)
    
    system_prompt = """You are the ACIS Code Assistant, an expert C++ geometry modeling engineer.
Your primary role is to provide clear, grounded explanations of ACIS concepts.

CRITICAL RULES:
1. ONLY explain "What it is", "Why it is used", and "How it works".
2. DO NOT list or summarize "Related Classes", "Methods", "Inheritance", "Parameters", "Return Types", or any structured relationships. (The graph renderer will handle these).
3. DO NOT output headers like "Graph Relationships", "Knowledge Graph Evidence", "Used By", or "Related Entities".
4. If you cannot find sufficient documentation to answer the question, output EXACTLY:
"No relevant information was found in the current knowledge graph.

Suggestions

• Verify the symbol spelling.
• Ask about a related class or function.
• Use a broader technical description."
"""

    if primary_entity_name:
        system_prompt = inject_primary_entity_lock(system_prompt, primary_entity_name)
        
    if is_retry:
        system_prompt += f"\n\nCRITICAL RETRY WARNING: Your previous generation incorrectly defined a related class or parent instead of {primary_entity_name}. You MUST focus exclusively on {primary_entity_name} as the subject of your explanation.\n"

    if intent == "Definition":
        layout = "## Definition\n## Purpose\n## Summary"
    elif intent == "Functional Explanation":
        layout = "## Overview\n## Workflow\n## Technical Explanation"
    elif intent == "Relationship":
        layout = "## Summary\n## Technical Explanation"
    else:
        layout = "## Answer\n## Technical Explanation"

    user_prompt = f"""[GRAPH CONTEXT]
{context}

[QUESTION]
{query}

[INSTRUCTIONS]
Query Intent: {intent}
PRIMARY SUBJECT: {primary_entity_name if primary_entity_name else 'Unknown'}

Using ONLY the supplied Knowledge Graph context, summarize the retrieved documentation.
If a section cannot be supported by the retrieved documentation, omit that section entirely.
Preferred Adaptive Layout (if supported by evidence):
{layout}

Answer ONLY using the supplied graph context.
Do NOT summarize or list related classes, functions, files, or relationships.
Every factual statement must be traceable to the supplied graph context.
Never use generic AI filler like "It is important for geometry."
The very first sentence of your response MUST describe {primary_entity_name}.
"""
    return system_prompt, user_prompt, intent

