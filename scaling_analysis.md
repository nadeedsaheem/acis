# Repository Scale & Performance Bottleneck Analysis

This document provides a scaling analysis of the GraphRAG architecture across four orders of magnitude of repository size. It identifies performance ceilings, memory bottlenecks, and processing constraints.

---

## 1. Metric Projections by Repository Scale

| Metric / Scale | **100K LOC** (ACIS) | **1M LOC** (OpenCascade) | **10M LOC** (Chromium / Unreal) | **100M LOC** (Corporate Mono-repo) |
| :--- | :--- | :--- | :--- | :--- |
| **Physical Files** | ~2,000 | ~15,000 | ~150,000 | ~1,500,000 |
| **Graph Nodes** | ~40,000 | ~350,000 | ~3,500,000 | ~35,000,000 |
| **Graph Edges** | ~80,000 | ~800,000 | ~8,500,000 | ~85,000,000 |
| **Vector Embeddings** | ~25,000 | ~200,000 | ~2,000,000 | ~20,000,000 |
| **`code_base.json` Size**| ~15 MB | ~150 MB | ~1.5 GB | ~15 GB |
| **Ingestion Time (Parse)**| ~30 seconds | ~5 minutes | ~1 hour | ~10 hours (single-thread limit) |
| **Graph Load Time** | ~45 seconds | ~8 minutes | ~2.5 hours | **Fails (Timeout/OOM)** |
| **Embedding Generation** | ~2 minutes | ~15 minutes | ~2.5 hours (local GPU) | ~25 hours (API limit) |
| **Neo4j Memory Footprint**| ~1.5 GB RAM | ~6 GB RAM | ~24 GB RAM | ~96 GB+ RAM |

---

## 2. Technical Bottlenecks by Processing Phase

### A. Ingestion Phase (`multi_repo.py` & `build_graph.py`)
1. **JSON Memory Load**: Currently, `build_graph.py` loads the entire `code_base.json` file into memory at once (`json.load(f)`). At 10M+ LOC, this JSON file grows to gigabytes, causing Python to run out of memory (OOM crash) during parsing and loading.
2. **Single-Threaded Walking**: File traversal and Tree-Sitter parsing are executed on a single thread. This cannot utilize multi-core server processors, resulting in long ingestion times.
3. **Sequential Neo4j Transactions**: Graph elements are committed sequentially in batches of 500. For millions of nodes and edges, this introduces significant latency due to network round-trips and transaction commit overhead.

### B. Retrieval & Search Phase (`retriever.py` & `embed_docs.py`)
1. **Unindexed String Matches**: Lexical search uses `CONTAINS` inside Cypher queries. Neo4j does not support schema indexes for `CONTAINS` substring searches (they act as full table scans). At 1M+ LOC, wildcard searches will cause high query latencies (seconds to minutes).
2. **Semantic Model Throttling**: Running local sentence embeddings on CPU throttles server throughput. Moving to cloud APIs (like OpenAI embeddings) introduces network overhead and rate-limiting blocks (`HTTP 429`) when processing batch documents.
3. **Graph Search Memory Exhaustion**: Broad `MATCH` queries without depth limits (e.g. tracking inheritance paths) will cause a combinatorial explosion of path states, exhausting Neo4j heap memory.

### C. Prompt & LLM Phase (`context_builder.py` & `grounded_answer_synthesizer.py`)
1. **Prompt Context Inflation**: Large classes (like `CATGeometry` or `UObject`) contain hundreds of methods and variables. The current context builder dumps the entire enriched representation into the prompt, overflowing the LLM token budget.
2. **Single Primary Entity Focus**: Designating a single primary entity fails to answer multi-entity comparison queries (e.g., *"Compare class A and class B"*), as the context for supporting entities is not enriched.

---

## 3. Scale-Up Remediation Strategy

To support repositories larger than **1M LOC**, the architecture must be refactored:
1. **Streamed Ingestion**: Replace `json.load()` with an incremental JSONL parser (e.g., `ijson`) to stream entities to Neo4j without loading the entire dataset into RAM.
2. **Parallel Indexing**: Run file parsing and embedding generation using multiprocessing pools.
3. **Full-Text Search Indexes**: Replaces `CONTAINS` string matches with Neo4j Full-Text Search Indexes (Lucene-backed) which support fast prefix, suffix, and token matching.
4. **Isolated Vector Storage**: Move vector storage and search from Neo4j to a dedicated vector database (e.g., Qdrant) that uses scalar quantization and HNSW to minimize memory footprints.
