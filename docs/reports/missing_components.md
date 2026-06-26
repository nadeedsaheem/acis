# Missing Components: Production Readiness Requirements

This document details the missing architectural modules required to transition the GraphRAG prototype into a production-grade, enterprise-scale C++ code intelligence system.

---

## 1. Semantic C++ Preprocessor & Compilation Database Integration
- **Priority**: **Critical**
- **Why production systems use it**: Large-scale C++ codebases (e.g., Chromium, OpenCascade, WDK) rely heavily on macro definitions, include headers, and conditional compilation branches (`#ifdef`). Production systems use a preprocessor step driven by `compile_commands.json` (clang compilation database) to expand macros and parse the exact codebase code that the compiler sees.
- **Risk if omitted**: The parser will fail to parse code blocks containing macro-wrapped class/method declarations, leading to silent omissions of core APIs and entities.
- **Estimated implementation complexity**: **High**
- **Recommended implementation order**: 1 (Parser Foundation)

---

## 2. Fully Qualified Name (FQN) Namespace Scope Resolver
- **Priority**: **Critical**
- **Why production systems use it**: Prevents naming collisions. Class names like `Vector`, `Node`, and `Context` are reused across different namespaces. Production systems use Fully Qualified Names (e.g., `math::geom::Vector`) as primary keys in the database.
- **Risk if omitted**: Global name collisions. Unrelated classes with identical names will merge into single graph nodes, resulting in incorrect relationships and corrupted LLM context.
- **Estimated implementation complexity**: **High**
- **Recommended implementation order**: 2 (Entity Integrity)

---

## 3. Call-Graph & Member Variable Schema Expansion (`CALLS`, `MEMBER_VARIABLE`)
- **Priority**: **High**
- **Why production systems use it**: For real-world code understanding, developers need to know:
  1. What functions are called by a method (`CALLS`).
  2. What variables a class owns (`MEMBER_VARIABLE`).
  Production systems map these relationships to allow impact analysis (e.g., "What will change if I edit this function?").
- **Risk if omitted**: The LLM will only understand declarations and documentation. It will be unable to answer questions about execution workflow, code dependencies, or class state.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 3 (Schema Completeness)

---

## 4. Full-Text Search (Lucene) & Reciprocal Rank Fusion (RRF) Reranking
- **Priority**: **High**
- **Why production systems use it**: String search using `CONTAINS` in Cypher is slow and does not rank results by keyword relevance. Production code engines use BM25 full-text indexing alongside vector semantic search, merging their results using Reciprocal Rank Fusion (RRF) to ensure precise symbol retrieval.
- **Risk if omitted**: Exact and shorthand symbol lookups will be slow and fail to rank top candidates properly, resulting in poor retrieval quality.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 4 (Retrieval Performance)

---

## 5. Token-Budgeting & Context Compression Layer
- **Priority**: **High**
- **Why production systems use it**: Large class declarations and deep inheritance paths quickly exceed LLM token limits. Production assistants count tokens dynamically and apply semantic compression (e.g., pruning irrelevant methods and summary generation) to keep contexts within budgets.
- **Risk if omitted**: LLM API calls will crash due to context window overflow, or introduce high latency and API token costs.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 5 (Context Efficiency)

---

## 6. Asynchronous Background Task Queue (Celery/Redis)
- **Priority**: **High**
- **Why production systems use it**: Reindexing a codebase or embedding documents takes hours at scale. Production architectures move these operations to background workers, freeing the web server to handle user queries.
- **Risk if omitted**: Reindexing will lock or crash the API server, making the assistant unavailable during updates.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 6 (Deployment Stability)

---

## 7. Isolated Vector Database (Qdrant)
- **Priority**: **Medium**
- **Why production systems use it**: Large codebases produce millions of documentation vectors. Storing and searching them in Neo4j causes memory pressure. Dedicated vector databases (e.g., Qdrant) use HNSW and quantization to perform vector searches rapidly while keeping memory consumption low.
- **Risk if omitted**: Neo4j pagecache exhaustion, leading to high query latencies and database crashes.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 7 (Vector Scaling)

---

## 8. Cross-Encoder Reranker Service
- **Priority**: **Medium**
- **Why production systems use it**: Bi-encoders retrieve a broad set of candidates quickly but lack high semantic accuracy. A Cross-Encoder reranker calculates precise similarity between the query and candidate documents, filtering out irrelevant nodes.
- **Risk if omitted**: Irrelevant context elements will be sent to the LLM, inflating token usage and causing distracted, low-quality answers.
- **Estimated implementation complexity**: **Low-Medium**
- **Recommended implementation order**: 8 (Retrieval Quality)

---

## 9. API Security, Rate Limiting, & Repository Namespace Isolation
- **Priority**: **High**
- **Why production systems use it**: Protects LLM quotas and prevents unauthorized access to proprietary source code. Ensures that developers can only query repositories they have permissions to view.
- **Risk if omitted**: Potential source code leaks, security vulnerabilities, and API quota abuse.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 9 (Security & Governance)

---

## 10. Citation Grounding & Fact Verification Pass
- **Priority**: **High**
- **Why production systems use it**: Developers must verify the assistant's claims. Production engines enforce inline citations (e.g., `[file.h:45]`) and run a validation pass to ensure that LLM explanations align with raw Neo4j facts.
- **Risk if omitted**: Silent hallucinations in the LLM's explanation could mislead developers, introducing bugs into code.
- **Estimated implementation complexity**: **Medium**
- **Recommended implementation order**: 10 (Grounding Trust)
