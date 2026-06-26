# Neo4j Query Modernization Report

## Issue
During the retrieval and ingestion phases, the Neo4j driver reported deprecation warnings related to the usage of `CALL { ... }` subqueries. In Neo4j 5.x, subqueries that reference variables from the outer scope must explicitly declare them using the correlated subquery syntax: `CALL (<variables>) { ... }`. Isolated subqueries without external variable dependencies must explicitly use an empty variable list `CALL () { ... }`.

## Fixes Implemented

1. **`src/embed_docs.py`**
   - **Line 102**: The vector search subquery `CALL { MATCH (d:Documentation) SEARCH d IN (VECTOR INDEX ...)` did not reference any outer scope variables (parameters like `$embedding` are allowed globally).
   - **Change**: Updated to `CALL () {`.

2. **`src/build_graph.py`**
   - **Line 795 (Returns Edges)**: The subquery merged primitive and entity return types using outer variables `row` and `parent`.
   - **Change**: Updated `CALL { WITH row, parent ... }` to `CALL (row, parent) { WITH row, parent ... }`.
   - **Line 915 (Documentation Edges)**: The multi-union subquery attached `Documentation` nodes to their parent entities (Class, Struct, Function, etc.) referencing `row` and `d`.
   - **Change**: Updated `CALL { WITH row, d ... }` to `CALL (row, d) { WITH row, d ... }`.

## Impact
- **No Deprecation Warnings**: The console remains clean during operations.
- **Identical Semantics**: The retrieval results and graph topology are exactly preserved.
- **Performance Preserved**: The explicit correlation syntax optimizes execution paths inside the Cypher engine natively in Neo4j 5.x.
