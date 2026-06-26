# ACIS GraphRAG System Architecture

This document provides a comprehensive blueprint of the C++ Code Intelligence System (ACIS) architecture. It describes how compiler-aware AST parsing, semantic embedding spaces, graph databases, hybrid search fusion, and LLM synthesis integrate to form a professional-grade GraphRAG assistant.

---

## 🗺️ System Blueprint

The ACIS architecture is designed to bridge the structural complexity of a large C++ codebase with the semantic understanding of LLMs. Below is the system dataflow diagram:

```
+-----------------------------------------------------------------------------------+
|                              1. Ingestion Pipeline                                |
|                                                                                   |
|  C++ Source Files + compile_commands.json                                         |
|        │                                                                          |
|        ▼                                                                          |
|  Tree-sitter Parser + Macro Registry + Conditional Evaluator                      |
|        │                                                                          |
|        ▼                                                                          |
|  FQN Resolver (Namespace Scope Tracking & Symbol Consolidation)                   |
|        │                                                                          |
|        ▼                                                                          |
|  data/code_base.json (FQN entities + call graph log)                              |
+-----------------------------------------------------------------------------------+
                                 │
                                 ▼
+-----------------------------------------------------------------------------------+
|                             2. Ingestion & Embedding                              |
|                                                                                   |
|  Neo4j Ingestion (Classes, Methods, Functions, Parameters, Returns)               |
|        │                                                                          |
|        ├───────────────► Documentation Nodes Ingested                             |
|        │                       │                                                  |
|        │                       ▼                                                  |
|        │                 Local PyTorch Embedding Model (BGE-small-en-v1.5)        |
|        │                       │                                                  |
|        │                       ▼                                                  |
|        │                 Store dense 384d vector in Documentation.embedding       |
|        │                       │                                                  |
|        │                       ▼                                                  |
|        │                 Compile Neo4j documentation_embedding_index              |
|        ▼                                                                          |
|  Build Code Call Graph (CALLS / CALLED_BY relationships)                          |
+-----------------------------------------------------------------------------------+
                                 │
                                 ▼
+-----------------------------------------------------------------------------------+
|                             3. Query & Retrieval Layer                             |
|                                                                                   |
|  User Query (e.g., "What is SPAposition?")                                        |
|        │                                                                          |
|        ▼                                                                          |
|  Intent Detection (Symbol Match vs Explanatory Workflow)                          |
|        │                                                                          |
|        ├───────────────────────────────────────┐                                  |
|        ▼                                       ▼                                  |
|  Vector Search (Top 50)               Lexical Search (Top 50)                     |
|  (BGE Cosine Similarity)              (FQN / Exact Match Identifier)              |
|        │                                       │                                  |
|        └───────────────────┬───────────────────┘                                  |
|                            ▼                                                      |
|                 Reciprocal Rank Fusion (RRF)                                      |
|                 ( პროგრამული Merge in Python)                                      |
|                            │                                                      |
|                            ▼                                                      |
|                 Select Top 20 Candidates                                          |
+-----------------------------------------------------------------------------------+
                                 │
                                 ▼
+-----------------------------------------------------------------------------------+
|                        4. Context Enrichment & Synthesis                          |
|                                                                                   |
|  Primary Entity Resolution (Suffix Matching & Collision Deconfliction)            |
|        │                                                                          |
|        ▼                                                                          |
|  Graph Context Ingestion (Class Scopes, Inheritance, Parameters, Return Types)    |
|        │                                                                          |
|        ▼                                                                          |
|  Call Graph Expansion (Recursive Depth-2 Call Tree Trace)                         |
|        │                                                                          |
|        ▼                                                                          |
|  Response Synthesis (Separating Natural Language explanation from Graph Evidence) |
|        │                                                                          |
|        ▼                                                                          |
|  Grounded Assistant Answer                                                        |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ Key Architectural Components

### 1. Parser & Compiler-Aware AST Ingestion
Unlike raw-text search tools, ACIS analyzes C++ code as a structured compiler output:
- **Preprocessor Tracking**: Evaluates preprocessor conditional blocks (`#ifdef`, `#else`) and expands macro statements to identify active source code paths.
- **Tree-sitter Traversals**: Scans AST node structures to build a symbol tree for class declarations, method prototypes, parameter footprints, and call sites.
- **FQN Resolution**: Chains active namespace blocks and nesting structures to assign globally unique Fully Qualified Names (FQNs) to every codebase entity, preventing collision errors across independent headers.

### 2. Semantic Embedding Space
Documentation nodes inside the AST extraction contain function descriptions, param contracts, and role summaries:
- **Model Selection**: Employs `BAAI/bge-small-en-v1.5` to generate 384-dimensional dense semantic vectors locally. BGE is chosen for its superior retrieval performance in English software documentation contexts.
- **Neo4j Storage & Indexing**: Vectors are written directly to `Documentation.embedding` properties. The database enforces a `documentation_embedding_index` vector index with cosine similarity metrics for sub-millisecond retrieval.

### 3. Two-Stage RRF Hybrid Retrieval
Retrieval operations utilize a multi-source candidate generator:
- **Lexical Stream**: Focuses on exact string lookups (like locating a class name `BODY` or method signature `api_set_var_blends`).
- **Vector Stream**: Performs semantic similarity searches to capture conceptual matches (like matching "How are topology changes tracked?" to cellular library routines).
- **RRF Merge**: The programmatic RRF fusion merges results based on rank positions:
  $$RRF(d) = \frac{1}{60 + r_{vector}(d)} + \frac{1}{60 + r_{lexical}(d)}$$
  This mathematical combination balances semantic mapping with absolute identifier matches, solving the problem of legacy score dominance.

### 4. Graph Context Enrichment
After RRF filters the search space down to the Top 20 entities, the graph layer performs structural lookups:
- **Scope Lookup**: Fetches inheritance chains, member methods, parameters, and return types for the candidate nodes.
- **Call Graph Extraction**: Dynamically traces recursive method calls (`e -[:CALLS]-> (next)`) up to Depth-2, allowing the assistant to explain procedural execution workflows.
- **Grounding & Evidence separation**: The final prompt separates code explanations from raw graph relationships, forcing the LLM to ground all factual assertions in structural evidence.

---

## 📋 Comprehensive Architecture Manuals

For deep-dives into specific subsystems, see the dedicated architectural guides:
- [Embedding Layer Architecture](docs/embedding_architecture.md): Model specs, indexing, storage formats, and selective generation.
- [Retrieval Subsystem Architecture](docs/retrieval_architecture.md): Parallel retrieval streams, RRF fusion, and optimized context queries.
- [End-to-End System Diagrams](docs/updated_system_architecture.md): Visual dataflow diagrams for ingestion and runtime queries.
