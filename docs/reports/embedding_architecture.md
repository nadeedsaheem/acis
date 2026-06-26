# Embedding Subsystem Architecture

The semantic search capability in the ACIS Code Intelligence System is powered by dense vector representations of codebase entity documentation. This document describes the selection, storage, indexing, and lifecycle of these embeddings.

---

## 🧠 Embedding Model Specification

The system integrates a local transformer model for dense vector extraction:
- **Model Identifier**: `BAAI/bge-small-en-v1.5`
- **Framework**: HuggingFace PyTorch `sentence-transformers`
- **Output Dimensions**: 384 dimensions
- **Pooling Strategy**: Mean pooling
- **Similarity Metric**: Cosine similarity (retrieved vectors are L2-normalized, reducing cosine comparison to a dot product)
- **Execution Mode**: Local CPU/GPU inference (completely offline, requiring no external network calls during search)

This model offers an optimal balance between low latency on commodity hardware and high semantic accuracy for software documentation.

---

## 💾 Graph Storage Representation

Embeddings are stored directly within the Neo4j Knowledge Graph. The relationship between logical C++ code entities and their semantic vector properties is modeled as follows:

```
 (e:Class | e:Method | e:Function | e:Struct | e:Enum)
                        │
                        │ HAS_DOC
                        ▼
               (d:Documentation)
                 ├── text: "Description of the entity..."
                 ├── hash: "cc5f59f537aa583ebc168b950c1..."
                 └── embedding: [0.0345, -0.0123, ..., 384 floats]
```

### Constraints & Indexes
To ensure sub-millisecond retrieval across tens of thousands of codebase nodes, a native vector index is compiled inside Neo4j:
- **Index Name**: `documentation_embedding_index`
- **Target Label**: `Documentation`
- **Target Property**: `embedding`
- **Configuration**:
  - Dimensions: 384
  - Similarity Function: `cosine`

The index is initialized via the Cypher syntax:
```cypher
CREATE VECTOR INDEX documentation_embedding_index
FOR (d:Documentation)
ON (d.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 384,
    `vector.similarity_function`: 'cosine'
  }
}
```

---

## 🔄 Embeddings Lifecycle & Operations

### 1. Ingestion and Offline Ingestion Loop (`tools/rebuild_embeddings.py`)
During full repository ingestion:
1. C++ entities and documentation blocks are parsed from C++ header files and written to `data/code_base.json`.
2. `build_graph.py` creates the schema nodes and establishes the `HAS_DOC` relationships.
3. The embedding tool reads the database in batches, checks for modified hashes, generates new embeddings, and pushes updates using batched Cypher queries.

### 2. Runtime Query Processing (`src/retrieval/embed_docs.py`)
When a developer query is received:
1. The raw text query is passed to the local `SentenceTransformer` instance.
2. The model encodes the query into a normalized 384-dimensional list of floats.
3. The float list is passed as a parameter (`$embedding`) to the Neo4j search query.
4. Neo4j executes a vector index search, returning the top 50 matches.

### 3. Selective Embedding generation (`tests/validation/phase14_validation.py` / `scratch/embed_selectively.py`)
To enable fast testing in sandboxed environments:
- An validation-oriented generation script performs selective embeddings for classes/structs and nodes matching key search keywords (`journal`, `blend`, `radius`, `track`).
- This allows validation tests to execute immediately without waiting for a full 26,000-node database encoding.
