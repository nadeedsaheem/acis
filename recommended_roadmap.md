# Production Roadmap: GraphRAG Evolution Plan

This roadmap outlines a structured, 16-week engineering plan to evolve the current GraphRAG prototype into an enterprise-grade C++ code intelligence system.

---

```mermaid
gantt
    title GraphRAG Production Evolution Timeline (16 Weeks)
    dateFormat  W
    axisFormat  w%W
    
    section Phase 1: Ingestion & Integrity
    Clang Preprocessor Integration      :active, p1_1, 0, 2w
    FQN Namespace Scope Resolver       :active, p1_2, 1w, 2w
    
    section Phase 2: Schema Expansion
    CALLS / MEMBER_VARIABLE Parsing    :p2_1, after p1_2, 2w
    Polymorphic / Template Edges       :p2_2, after p2_1, 2w
    
    section Phase 3: Retrieval & Search
    Neo4j BM25 & Qdrant Integration    :p3_1, after p2_2, 2w
    RRF & Cross-Encoder Reranker       :p3_2, after p3_1, 2w
    
    section Phase 4: Scaling & Operations
    Token Budgeting & Compression      :p4_1, after p3_2, 2w
    Auth, Rate Limiting & Async Queue  :p4_2, after p4_1, 2w
```

---

## Phase 1: Parser & Symbol Integrity (Weeks 1–4)
- **Goal**: Establish a macro-resilient parser that extracts syntactically sound C++ symbols without entity collisions.
- **Milestones**:
  - **Weeks 1–2**: Integrate Clang preprocessor parsing driven by a `compile_commands.json` database. Extract include paths and macro expansion maps.
  - **Weeks 3–4**: Build a Fully Qualified Name (FQN) resolver. Ensure namespaces and nested declarations are mapped to distinct, unique FQN scopes (e.g., `namespace::Class::Method`).

---

## Phase 2: Schema & Relationship Expansion (Weeks 5–8)
- **Goal**: Expand the Neo4j graph schema to support execution workflow tracing and state mapping.
- **Milestones**:
  - **Weeks 5–6**: Refactor `multi_repo.py` to extract class member variables and functional call expressions within method blocks. Map `MEMBER_VARIABLE` and `CALLS` edges in Neo4j.
  - **Weeks 7–8**: Implement polymorphic inheritance mapping (`OVERRIDES` edges) and template specialization edges. Enforce file dependency include tracking.

---

## Phase 3: Retrieval & Search Modernization (Weeks 9–12)
- **Goal**: Upgrade retrieval from basic string matches to a high-speed, statistical search engine.
- **Milestones**:
  - **Weeks 9–10**: Deploy a Qdrant Vector Database instance to offload vector operations from Neo4j. Replace Cypher `CONTAINS` queries with Neo4j Full-Text Lucene indexes (BM25).
  - **Weeks 11–12**: Implement Reciprocal Rank Fusion (RRF) to merge BM25 and vector candidate rankings. Deploy a lightweight Cross-Encoder model (e.g., `ms-marco`) for precise re-ranking.

---

## Phase 4: Operational Scaling & Security (Weeks 13–16)
- **Goal**: Secure, parallelize, and scale the API server for enterprise deployment.
- **Milestones**:
  - **Weeks 13–14**: Implement token budgeting in `context_builder.py` and prune inactive code methods from prompts. Integrate Celery and Redis to handle repository updates in background tasks.
  - **Weeks 15–16**: Add rate-limiting, JWT authentication, and repository-level graph isolation. Enhance LLM synthesis with inline citation formatting and a fact-verification pass.
  - **Week 16**: Perform end-to-end latency testing on a 10M LOC repository, ensuring P99 response times stay below 5 seconds.
