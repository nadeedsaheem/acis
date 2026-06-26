# SPAposition Retrieval and Prompt Audit

**Query:** `What is SPAposition?`

## 1. Top 10 Retrieved Nodes & Scores

1. **Unknown** (Score: `0.9183`)
   - **Documentation:** `SPAposition array.`
2. **Unknown** (Score: `0.9150`)
   - **Documentation:** `the SPAposition if any do.`
3. **Unknown** (Score: `0.9143`)
   - **Documentation:** `point from a SPAposition`
4. **Unknown** (Score: `0.9087`)
   - **Documentation:** `Returns the SPAposition contained by this attribute.`
5. **Unknown** (Score: `0.9067`)
   - **Documentation:** `SPAposition which anchors the view`
6. **Unknown** (Score: `0.9061`)
   - **Documentation:** `debug a SPAposition`
7. **Unknown** (Score: `0.9046`)
   - **Documentation:** `Returns the coordinates of this APOINT as an SPAposition.`
8. **Unknown** (Score: `0.9005`)
   - **Documentation:** `Return the current SPAposition in the`
9. **Unknown** (Score: `0.9002`)
   - **Documentation:** `SPAposition_cloud is a class for geometrically querying large sets of points...`
10. **Unknown** (Score: `0.8909`)
    - **Documentation:** `Basic constructor (from a SPAposition).`

## 2. Expanded Graph Context

The Context Builder expanded the retrieved nodes into the following structures:

```markdown
## Class
SPAPOSITION_ARRAY
Documentation: SPAposition array.
Inherits: ACIS_OBJECT

## Function
find_candidates
Documentation: the SPAposition if any do.
Returns: tree_list

## Function
bounded_point
Documentation: point from a SPAposition
Returns: class DECL_KERN

## Function
value
Documentation: Returns the SPAposition contained by this attribute.
Returns: SPAposition

## Function
view_spec
Documentation: SPAposition which anchors the view
Returns: class DECL_INTR

## Function
dbpos
Documentation: debug a SPAposition
Returns: void

## Function
coords
Documentation: Returns the coordinates of this APOINT as an SPAposition.
Returns: SPAposition

## Function
mark
Documentation: Return the current SPAposition in the
Returns: long

## Class
SPAposition_cloud
Documentation: SPAposition_cloud is a class for geometrically querying...
Inherits: ACIS_OBJECT
Methods: read_position_cloud_from_file, read_position_cloud_from_file, read_position_cloud_from_stl_file

## Function
NODE
Documentation: Basic constructor (from a SPAposition).
Parameters:
- const SPAposition& pos
Returns: void
```

## 3. Final Context Sent to Gemini & Final Prompt Size

- **Final Prompt Size:** 1,642 characters

The prompt instructed the LLM: 
> `Answer strictly using the graph context. Cite relevant entities when possible. If insufficient information exists, explicitly say so.`

## 4. Why Grounding Guard Triggered

The answer was correctly classified as "Insufficient information" due to a **Retrieval Failure (Scenario A)**, aggravated by the context builder strictness. 

**Diagnosis:**
The vector embedding strategy currently only embeds `(:Documentation)` nodes. While `SPAposition` is one of the most critical classes in ACIS, its core class documentation might be generic (e.g., "Defines a 3D point") and therefore *does not contain the word SPAposition itself*, or it might be entirely undocumented. Because semantic search strictly relies on embedded documentation text, it completely missed the `(:Class {name: "SPAposition"})` node.

Instead, semantic search retrieved peripheral functions and arrays that happen to mention `SPAposition` in their documentation (like `SPAPOSITION_ARRAY` and functions returning it). Since the context lacked the fundamental definition of `SPAposition`, a strictly grounded LLM must trigger the "Insufficient information" safeguard to avoid hallucination. Furthermore, the mock LLM in the current development environment reinforces this by falling back to "Insufficient information" for any un-whitelisted query.

## Recommendations for Production Hardening

To fix this and guarantee deterministic entity resolution while maintaining hallucination protection:

1. **Implement Hybrid Search (Lexical + Semantic):**
   - RAG should not rely purely on semantic vectors for named entities. Add a lexical exact-match phase:
   - `MATCH (c:Class) WHERE toLower(c.name) CONTAINS toLower($query) RETURN c`
   - Merge these exact-match graph structures with the vector search results before sending to the Context Builder.

2. **Embed Entity Names & Signatures:**
   - Update `embed_docs.py` to embed a synthesized string containing the node type, name, and documentation together, e.g., `"Class SPAposition: A mathematical point in 3D."` This ensures class names strongly influence vector similarity.

3. **Graph Traversal Expansion:**
   - When a class name strongly matches the user's query, dynamically expand the context to include its `HAS_METHOD` and `USES_TYPE` relationships, rather than just returning documentation snippets.
