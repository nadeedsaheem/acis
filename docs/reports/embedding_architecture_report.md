# Embedding Architecture Report

This report provides the final assessment of the embedding architecture, classifies the retrieval system, audits the repository layout, and answers the core verification questions.

---

## 🏷️ Step 5 — Retrieval Type Classification

### Classification: **4. Hybrid GraphRAG**

### Justification:
The system goes beyond basic vector retrieval or keyword matching by combining three distinct retrieval layers to construct the final LLM context:
1.  **Vector Semantic Search:** Executes a cosine similarity lookup against a Neo4j Vector Index (`documentation_embedding_index`) using a local SentenceTransformer model (`BAAI/bge-small-en-v1.5`).
2.  **Lexical Keyword Fallback:** Simultaneously runs a case-insensitive keyword search on entity names and FQNs, boosting exact/partial string matches with a high priority score (`2.0`). This prevents keyword terms (e.g. C++ class names) from being missed by dense vector semantics.
3.  **Graph Expansion / Enrichment:** Uses Neo4j relationships (`INHERITS`, `RETURNS`, `HAS_PARAMETER`, `HAS_METHOD`, `CALLS`) to extract structural neighbors around the matches. This feeds the LLM with structured compiler facts (e.g. class methods, parameters, call trees) alongside natural language documentation.

---

## 📁 Step 6 — Repository Structure Audit & Recommendation

### Current Structure:
All embedding, vector indexing, and retrieval logic is placed in `src/retrieval/`:
*   `src/retrieval/embed_docs.py`: Contains `SemanticRetriever` which handles model loading, embedding generation, index creation, and the hybrid search query.
*   `src/retrieval/retriever.py`: Exposes the lazy-loaded `semantic_search` singleton wrapper and the legacy lexical-only `KnowledgeGraphRetriever`.

### Proposed Structure (`src/embeddings/`):
Moving embeddings into a dedicated package:
```
src/embeddings/
    ├── __init__.py
    ├── embedder.py             # SentenceTransformer loader & encoder
    ├── vector_index_manager.py  # Neo4j index setup, drops, and verifications
    └── embedding_service.py    # Batch generators & payload enrichers
```

### Recommendation: **Not Beneficial for the Current Scale**
We recommend **retaining** the current structure with minor refactoring, for the following reasons:
1.  **Tight Neo4j Integration:** The model encoding, vector search, lexical fallback, and graph expansion are tightly bound inside a single Cypher transaction in `embed_docs.py`. Splitting this into multiple modules would introduce artificial layers without clean separation of concerns.
2.  **Maintainability:** Keeping `SemanticRetriever` near other scoring and retrieval components (e.g. `primary_entity_resolver.py`, `intent_entity_ranker.py`) keeps the entire query retrieval flow localized in `src/retrieval/`.
3.  **Refactoring Recommendation:** Instead of creating a new package, we recommend **merging** or **deprecating** the legacy lexical-only `KnowledgeGraphRetriever` class inside `src/retrieval/retriever.py` to prevent developer confusion, and renaming `src/retrieval/embed_docs.py` to `src/retrieval/semantic_retriever.py` to better reflect its class name and role.

---

## 🙋 Final Questions & Explicit Answers

### 1. Do embeddings exist?
**Yes.** Raw documentation text is embedded during initialization. These can be further enriched with C++ structure payloads via `tools/rebuild_embeddings.py`.

### 2. Which model is used?
**`BAAI/bge-small-en-v1.5`** (running locally via the `sentence-transformers` library).

### 3. Where are embeddings stored?
Directly inside the **Neo4j Graph Database** on the `embedding` property of the `(d:Documentation)` nodes.

### 4. Are embeddings used during retrieval?
**Yes.** Every query passing through `api_server.py` or `graphrag_service.py` is vectorized and queried using the Neo4j vector index search.

### 5. What percentage of retrieval depends on embeddings?
**50%.** Retrieval is fully hybrid. The initial candidate selection is a union of vector matching (50%) and lexical entity name/FQN matching (50%). The graph expansion and ranking layers then process these candidates equally.

### 6. Should embeddings become their own package?
**No.** Keep them under `src/retrieval/` but refactor the files (e.g., deprecate the legacy `KnowledgeGraphRetriever` and rename `embed_docs.py` to `semantic_retriever.py`) to keep the codebase cohesive and clean.
