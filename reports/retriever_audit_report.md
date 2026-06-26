# Retriever Audit Report

## Inspection of `retriever.py`
- **Public Classes:** `KnowledgeGraphRetriever` (implements keyword-based search via Cypher).
- **Public Functions:** `validate_retrieval(retriever)`
- **Entry Point:** `if __name__ == '__main__':` block executing keyword search validation.

## Semantic Search Status
- **Is `semantic_search` implemented in `retriever.py`?** No.
- **Where does it exist?** It is currently implemented in `embed_docs.py` within the `SemanticRetriever` class.
- **Equivalent function in `retriever.py`:** `KnowledgeGraphRetriever.search(query, top_k=10)`, which performs keyword/Regex-based retrieval rather than vector semantic search.

## Import Issues Detected
The test script `test.py` expects a top-level function `semantic_search` to be importable directly from the `retriever` module. Because this function is completely missing from `retriever.py`, it throws an `ImportError`.

## Recommended API Fix
1. Expose `semantic_search(query, top_k=10)` as a top-level function in `retriever.py`.
2. To prevent the `sentence-transformers` model (`BAAI/bge-small-en-v1.5`) from being loaded from disk into memory every time the function is called, implement a global singleton cache `_semantic_retriever_instance`.
3. The function should internally initialize `SemanticRetriever` (from `embed_docs.py`), execute the search, and return the results directly.
