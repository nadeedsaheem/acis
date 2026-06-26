# ACIS GraphRAG Project Structure

This document details the project layout, production code modules, and their design responsibilities. The layout isolates C++ AST parsing, graph database ingestion, embedding-based vector spaces, RRF retrieval, LLM synthesis, and FastAPI service exposure.

---

## 📂 Repository Layout Tree

```
project_root/
│
├── README.md                          # High-level architecture & Quick Start
├── PROJECT_STRUCTURE.md               # Detailed directory tree & module guide
├── SYSTEM_ARCHITECTURE.md              # Blueprint of end-to-end GraphRAG pipeline
├── requirements.txt                   # Dependency manifest (sentence-transformers, neo4j, etc.)
├── .env.example                       # Template for database & API credentials
│
├── src/                               # Core production pipeline packages
│   ├── parser/                        # Compiler-aware C++ Tree-sitter parsing
│   │   ├── multi_repo.py              # AST traversal over codebase folders
│   │   ├── namespace_tracker.py       # Scoping and C++ namespace tracking
│   │   ├── fqn_resolver.py            # Resolving globally unique symbol FQNs
│   │   ├── call_extractor.py          # Static call sites analysis from AST
│   │   ├── compilation_database.py    # Handling compile_commands.json entries
│   │   ├── include_resolver.py        # Tracking preprocessor header paths
│   │   ├── macro_registry.py          # Storing and resolving C++ macro expansions
│   │   └── conditional_evaluator.py   # Parsing preprocessor conditional branches (#ifdef)
│   │
│   ├── graph/                         # Persistent Neo4j Knowledge Graph builder
│   │   ├── build_graph.py             # Schema definition & constraints compiler
│   │   ├── call_graph_builder.py      # Call graph relations (CALLS / CALLED_BY) ingestion
│   │   ├── graph_context_enricher.py  # Constructing recursive depth-2 context subgraphs
│   │   ├── graph_relationship_renderer.py # Standardized formatting of graph relationships
│   │   └── graph_evidence_renderer.py # Rendering facts & signatures for response grounding
│   │
│   ├── retrieval/                     # Hybrid search, routing & scoring layer
│   │   ├── embed_docs.py              # Semantic vector indexing & query execution
│   │   ├── retriever.py               # Orchestrator coordinating hybrid search
│   │   ├── rrf_fusion.py              # Reciprocal Rank Fusion (RRF) rank merger
│   │   ├── conversation_classifier.py # Rule-based query classifier (Greetings/Small Talk/Help)
│   │   ├── query_router.py            # Conversational bypass gatekeeper & router
│   │   ├── primary_entity_resolver.py # FQN suffix-matching and entity deduplication
│   │   ├── entity_scoring.py          # Weight calculations & static scoring heuristics
│   │   └── query_normalizer.py        # Tokenizing and cleaning developer input
│   │
│   ├── llm/                           # Context formatting & LLM orchestration
│   │   ├── llm_provider.py            # Gemini API integration wrapper
│   │   ├── grounded_answer_synthesizer.py # Grounded context prompts and LLM requests
│   │   └── response_composer.py       # Unifying graph evidence and natural explanation
│   │
│   └── api/                           # REST Service layer (FastAPI)
│       ├── api_server.py              # Server launcher, routing, & error recovery
│       ├── api_models.py              # Pydantic query schemas
│       └── graphrag_service.py        # E2E service orchestration
│
├── tests/                             # QA test suites
│   ├── validation/                    # Phase-by-phase functional verification (Phases 9-15)
│   │   ├── phase14_validation.py
│   │   └── phase15_validation.py      # Classifier & router safety/latency verification
│   └── integration/                   # End-to-end service testing
│
├── examples/                          # Interactive demonstrations
│   └── chat_demo.py                   # Console CLI client
│
├── tools/                             # Standalone maintenance utilities
│   ├── rebuild_embeddings.py          # Embedding regeneration script
│   └── generate_fqn_reports.py        # Collision metrics compiler
│
├── docs/                              # System manuals & deep-dive reports
│   ├── reports/                       # Validation phase certificates (Phases 6-15)
│   ├── embedding_architecture.md      # Deep-dive on BGE-small embedding layer
│   ├── retrieval_architecture.md      # Deep-dive on RRF & two-stage retrieval
│   ├── updated_system_architecture.md # Ingestion & search flowchart guides
│   └── conversation_examples.md       # Predefined response mapping guide
│
└── archive/                           # Superseded/legacy research artifacts
```

---

## 🔍 Module Responsibilities: Retrieval Layer (`src/retrieval/`)

The hybrid retrieval system operates under a multi-source schema, where vector, lexical, and graph retrieval coordinates are merged programmatically:

### 1. `embed_docs.py`
This module acts as the core interface to the semantic embedding space. It is responsible for:
- **Embedding Generation**: Iterating over database documentation chunks and running batch encoding.
- **Query Embeddings**: Generating 384-dimensional normalized dense vectors for developer input queries at runtime.
- **Vector Retrieval**: Querying the Neo4j database using vectorized cosine similarity.
- **Neo4j Vector Index Access**: Creating and managing the lifetime of `documentation_embedding_index` on `Documentation(embedding)`.
- **Semantic Search Orchestration**: Managing two-stage query processing and fetching metadata for top candidates.

### 2. `retriever.py`
The central orchestrator of the search pipeline. It coordinates:
- Running intent detection on incoming queries to decide query parameters.
- Dispatching parallel vector and lexical database tasks.
- Calling the RRF fusion merger to combine separate streams into one ranked candidate set.
- Invoking the context expander to fetch Call Graph trees and class scopes for target entities.

### 3. `rrf_fusion.py`
A mathematical utility module implementing **Reciprocal Rank Fusion (RRF)**:
- Computes candidate fusion scores using rank reciprocals: $R(d) = \sum_{m} \frac{1}{60 + r_m(d)}$.
- Prevents high-score lexical matches from eclipsing highly relevant semantic hits, ensuring even distribution across the search space.

### 4. `primary_entity_resolver.py`
Resolves candidate ambiguities and name collisions:
- Compares retrieved FQNs with C++ suffix-matching heuristics (e.g., matching a local method `Draw` to its parent class method `DM_icon::Draw`).
- Deduplicates matching symbols across files using hash-based identities.

### 5. `entity_scoring.py`
Performs static scoring adjustments:
- Penalizes or boosts candidates based on node labels (e.g., boosting a `Class` or `Function` definition over parameter variables).
- Calculates parameter similarity overlap to refine matching relevance.

### 6. `query_normalizer.py`
Applies text normalization to queries:
- Strips punctuation, cleans whitespace, and filters stop words.
- Identifies potential code structures (like `::` scoping or `()` invocations) to guide intent detection.

### 7. `conversation_classifier.py`
Lightweight query classification engine:
- Uses string parsing and set intersection checks to identify greeting, small talk, and help intents in microsecond timescales.
- Integrates a C++ keyword and syntax override list to prevent false-positive routing of technical inquiries.

### 8. `query_router.py`
Routing gateway for incoming service calls:
- Intercepts conversational messages to return predefined formatted response structures.
- Bypasses embedding computation and database queries for non-retrieval intents to maintain sub-1ms response times.

