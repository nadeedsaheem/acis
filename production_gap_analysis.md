# Production Gap Analysis: GraphRAG Architecture Audit

This document performs a comprehensive gap analysis of the current GraphRAG architecture compared to modern, enterprise-grade code intelligence systems (such as Sourcegraph Cody, GitHub Copilot Workspace, Cursor, and Microsoft code retrieval architectures) designed for multi-million line industrial C++ repositories.

---

## 1. Parser & Syntax Extraction Layer

| Feature / Aspect | Current Implementation | Industrial Standard (Cody, Cursor, Copilot) | Gap Severity & Impact |
| :--- | :--- | :--- | :--- |
| **C++ Preprocessor & Macro Expansion** | Ad-hoc regex filtering and blacklist checks (`is_legitimate_name`, skipping `DECL_KERN`, etc.). No preprocessor execution. | Compiles code semantically using a compiler frontend (e.g., Clang AST or GCC output) combined with a `compile_commands.json` database to resolve preprocessor macros. | **CRITICAL**. Without macro expansion, tree-sitter fails to parse declarations containing macros, resulting in silent omissions of classes, methods, and structures. |
| **Conditional Compilation** | Ingests raw source code line-by-line; ignores compiler flags and target definitions (`#ifdef`, `#if defined`). | Config-aware parsing. Ingests symbols based on specific build configurations (e.g., Windows vs. Linux, Debug vs. Release). | **HIGH**. Graph will contain symbols from inactive code branches or will fail to resolve symbols that are defined conditionally, polluting context. |
| **Template Support** | Rudimentary stripping of `<...>` template arguments during class name normalization. | Full template metaprogramming mapping, resolving templates to their template definitions and tracking instantiations and partial specializations. | **HIGH**. Industrial C++ relies heavily on template programming (e.g., CRTP, traits). Normalizing templates away prevents the LLM from understanding typenames, base classes, and interfaces. |
| **Namespace Aliasing & Resolving** | Extracts namespaces but does not resolve namespace aliases (e.g., `namespace fs = std::filesystem;`) or `using` statements. | Full hierarchical namespace resolution and scope tracking. Resolves aliased namespaces to their canonical target names. | **HIGH**. Causes symbol resolution to fail when symbols are referenced using aliases or inside nested namespaces, resulting in incorrect graph links. |
| **Multi-Repository Support** | Ingests a single repository root folder. | Multi-repo mapping. Links external dependencies and symbols across multiple repositories using unique repository IDs and versions. | **MEDIUM**. For industrial C++ environments where projects depend on multiple internal and external library repositories, cross-repo navigation is broken. |

---

## 2. Graph Schema & Structural Relationships

| Relationship | Current Schema | Required Production Schema | Purpose in Code Intelligence |
| :--- | :--- | :--- | :--- |
| **`CALLS` / `CALLED_BY`** | **Missing**. No method/function call extraction. | `(:Method/Function)-[:CALLS]->(:Method/Function)` | Necessary for tracking execution flow, finding callers of an API, and generating execution call-stacks. |
| **`MEMBER_VARIABLE`** | **Missing**. Member variables are ignored. | `(:Class/Struct)-[:HAS_MEMBER]->(:Variable)` | Critical for understanding class state, properties, and data layout. |
| **`FRIENDS`** | **Missing**. C++ `friend` classes/functions ignored. | `(:Class)-[:FRIEND_OF]->(:Class/Function)` | Maps structural C++ access override details. |
| **`TEMPLATE_INSTANTIATION`** | **Missing**. Templates are normalized away. | `(:Class/Method)-[:SPECIALIZES]->(:Template)` | Understands specific instances of template classes/methods (e.g., `Vector<int>`). |
| **`IMPLEMENTS` / `OVERRIDES`** | **Missing**. Heuristic virtual flags only. | `(:Method)-[:OVERRIDES]->(:Method)` | Explicitly tracks polymorphic hierarchies. |
| **`DEPENDS_ON` / `INCLUDES`** | `includes` array attribute in JSON. | `(:File)-[:INCLUDES]->(:File)` | Understands build-dependency graph and file-level relationships. |

---

## 3. Retrieval & Ranking Layer

### A. Missing Search Infrastructures
1. **BM25 Retrieval**: Currently, the system uses basic Cypher `CONTAINS` string matching. This is extremely slow and lacks term frequency-inverse document frequency (TF-IDF) statistical balancing, making lexical search inaccurate on large text sets.
2. **Cross-Encoder Reranking**: Bi-encoders (like `bge-small-en`) are fast for initial candidate retrieval but struggle to capture fine-grained semantic relevance. Production systems use Cross-Encoders (e.g., `ms-marco-MiniLM`) to evaluate the exact semantic match between the query and retrieved candidates.
3. **Graph Distance Scoring**: The current entity scoring heuristic ignores topological relationships between candidates during ranking. Candidates that are closer in the graph (e.g., a class and its member methods) should receive a boost.
4. **Query Rewriting & Sub-Query Planning**: Developer queries are often shorthand or incomplete. Modern systems use LLM-based query expansion to resolve aliases, add synonyms, and generate multiple search queries to search both vector and graph databases.

---

## 4. Entity Resolution & Namespace Collision

With 500 classes named `Vector` in a 10M line repository, the current system will behave as follows:
- **Collision & Collapse**: Since name normalization strips template parameters and namespaces, multiple `Vector` classes will collapse into single or mismatched entities unless their paths are fully distinct.
- **Ambiguous Retrieval**: If the query is "What is Vector?", the semantic retriever will fetch all 500 nodes and their documentation, sorting them by documentation length and connectivity. This will result in context pollution, combining details from math vectors, UI layout vectors, and STL vectors into a single prompt.
- **Production Solution**: Production systems resolve symbols to their Fully Qualified Names (FQNs) (e.g., `std::vector` vs. `graphics::math::Vector`) using compiler-resolved scopes. When a query is made, scope-matching heuristics prioritize symbols in the user's active file or referenced namespace.

---

## 5. Context Building & Token Budgets

- **Token Budgeting**: The current system does not count tokens before sending contexts to the LLM. If an enriched primary entity has hundreds of methods and deep inheritance, it will overflow the context window, causing API crashes or high latencies.
- **Context Compression**: The system passes raw database outputs. It lacks semantic pruning (removing unused methods/attributes that are irrelevant to the user's query) and graph summarization (providing a high-level topological map instead of flat text).

---

## 6. LLM Generation & Grounding

- **Hallucination Vectors**: Although the system isolates LLM synthesis from structured evidence rendering, the LLM itself can still hallucinate explanations of "How it works" or "Why it is used" when the documentation is thin.
- **Missing Verifications**:
  1. **Citation Grounding**: No inline links or citations (file path + line number) are generated in the LLM's explanation, making validation manual and tedious.
  2. **Self-Reflection & Fact-Checking**: No second-pass LLM or rule-based parser verifies that the generated explanation aligns with the raw Neo4j facts before presenting it to the client.

---

## 7. API & Integration Layer

- **Rate Limiting**: Missing. Vulnerable to Denial of Service (DoS) and API quota exhaustion.
- **Streaming**: Missing. Blocking JSON responses result in high Time-to-First-Token (TTFT) latency, degrading developer experience.
- **Caching**: Missing. Duplicate queries hit the embedding model, Neo4j, and the LLM every time.
- **Isolation**: Missing repository isolation. All data resides in a single database space without tenant-level or project-level security partitions.

---

## 8. Deployment & Vector Infrastructure

- **Decoupling Models**: Currently, the `SentenceTransformer` model runs in-memory inside the FastAPI process. This prevents horizontal scaling, consumes massive CPU/RAM, and blocks request threads during encoding.
- **Vector Database**: Neo4j's native vector index is poorly optimized for high-throughput, real-time searches at scale. Large codebases require a dedicated vector database (like Qdrant or Milvus) to offload vector search compute from graph query compute.
