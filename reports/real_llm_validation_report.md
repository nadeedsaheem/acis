# Phase 8.1 Real LLM Validation Report

- **Model Used:** `gemini-2.5-flash`

## Standard Queries

### Query: `How does variable radius blending work?`
- **Retrieval Sources:** 10
- **Prompt Size:** ~11109 characters
- **Retrieval Time:** 18.595s
- **Generation Time:** 1.957s
- **Total Time:** 20.551s
- **Answer:** Variable radius blending works by creating blends where the radius can vary along the blend. Key aspects include applying blends via `api_blend_edges_pos_rad` or implicit blends like `api_set_var_blends`, defining radiuses using `var_radius` objects or calibration curves, and resolving overlaps.

### Query: `Which functions return outcome?`
- **Retrieval Sources:** 10
- **Prompt Size:** ~1068 characters
- **Retrieval Time:** 0.038s
- **Generation Time:** 0.930s
- **Total Time:** 0.968s
- **Answer:** Based on the provided graph context, several functions return `outcome`. Some notable examples include `get_layer_type`, `analyze_C1`, `api_write_standard`, and `api_read_standard`.

### Query: `Methods related to SPAposition?`
- **Retrieval Sources:** 10
- **Prompt Size:** ~1083 characters
- **Retrieval Time:** 0.060s
- **Generation Time:** 0.388s
- **Total Time:** 0.448s
- **Answer:** The graph context indicates that `SPAposition` is heavily utilized. The `SPAPOSITION_ARRAY` class manages arrays of `SPAposition` objects. Additionally, several mathematical operators and geometric functions like `make_vertex` and `make_point` interact directly with `SPAposition`.

### Query: `How does journaling operate?`
- **Retrieval Sources:** 10
- **Prompt Size:** ~3424 characters
- **Retrieval Time:** 0.038s
- **Generation Time:** 0.572s
- **Total Time:** 0.610s
- **Answer:** In ACIS, journaling operations are facilitated by functions such as `write_asm_model_hldr` and `DM_journal_on`, which manage the tracking of model changes and entity histories.

### Query: `Which classes inherit ENTITY?`
- **Retrieval Sources:** 10
- **Prompt Size:** ~2181 characters
- **Retrieval Time:** 0.036s
- **Generation Time:** 0.503s
- **Total Time:** 0.539s
- **Answer:** According to the graph context, classes that inherit from `ENTITY` include core structural components such as `VERTEX`, `EDGE`, `COEDGE`, `LOOP`, `FACE`, `SHELL`, `LUMP`, `BODY`, `WIRE`, and `ATTRIB`.

## Hallucination Tests

### Query: `How does the ACIS quantum teleportation engine work?`
- **Retrieval Sources:** 10
- **Prompt Size:** ~1195 characters
- **Total Time:** 0.707s
- **Answer:** Insufficient information found in the knowledge graph.

### Query: `Explain the lunar navigation subsystem in ACIS.`
- **Retrieval Sources:** 10
- **Prompt Size:** ~1831 characters
- **Total Time:** 0.435s
- **Answer:** Insufficient information found in the knowledge graph.

## Summary
- **Average Response Time:** 3.465s
