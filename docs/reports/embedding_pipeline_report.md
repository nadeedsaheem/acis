# Embedding Pipeline Report

This report documents the exact source code paths, methods, and configurations used to initialize the embedding model and generate embeddings within the GraphRAG repository.

---

## 🛠️ Step 1 — Embedding Model Initialization

The repository utilizes a local SentenceTransformer model for generating dense vector representations.

### Model Details
*   **Embedding Model:** `BAAI/bge-small-en-v1.5`
*   **Embedding Dimension:** `384` (retrieved programmatically via `model.get_sentence_embedding_dimension()`)
*   **Initialization File:** [embed_docs.py](file:///c:/Users/Dell/OneDrive/Desktop/step1/src/retrieval/embed_docs.py)
*   **Initialization Code (lines 11–16):**
    ```python
    class SemanticRetriever:
        def __init__(self, uri, user, password, model_name="BAAI/bge-small-en-v1.5"):
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logging.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logging.info(f"Model loaded. Dimension: {self.dimension}")
    ```

---

## 🔄 Step 2 — Document Embedding Generation Lifecycle

Document embedding creation follows a multi-stage lifecycle, starting from AST parsing of raw source code to final database updates.

```mermaid
graph TD
    A[Source Code] -->|AST Traversal| B[code_base.json]
    B -->|Ingestion via build_graph.py| C[Neo4j (d:Documentation) Nodes]
    C -->|Fetch in batch via Cypher| D[embed_docs.py or rebuild_embeddings.py]
    D -->|SentenceTransformer Encode| E[384-Dim Vector Embeddings]
    E -->|Write-back via UNWIND| F[Neo4j d.embedding Property]
```

### Stage 1: Extraction & Structuring
*   **Responsible Files:** C++ parser packages under `src/parser/`
*   **Action:** Traversing C++ source files, extracting raw class, struct, enum, function, and method documentation comments.
*   **Output:** Saved to the master JSON file [code_base.json](file:///c:/Users/Dell/OneDrive/Desktop/step1/data/code_base.json).

### Stage 2: Database Ingestion
*   **Responsible Files:** [build_graph.py](file:///c:/Users/Dell/OneDrive/Desktop/step1/src/graph/build_graph.py)
*   **Action:** Reads `code_base.json` and creates entities. In `load_documentation_tx` (lines 1073–1114), it creates `(d:Documentation)` nodes containing raw texts and hooks them to their parent entities (e.g. Class, Struct, Function, Method) using `(entity)-[:HAS_DOC]->(d:Documentation)` edges.
*   **Cleaning Logic (lines 49–59):**
    ```python
    def clean_documentation(doc_text):
        if not doc_text:
            return ""
        # Remove basic HTML tags safely (avoiding <T> templates)
        doc_text = re.sub(r'</?(p|br|div|span|b|i|strong|em|ul|li|ol)[^>]*>', ' ', doc_text, flags=re.IGNORECASE)
        # Normalize multiple newlines and spaces
        doc_text = re.sub(r'\n{3,}', '\n\n', doc_text)
        doc_text = re.sub(r'[ \t]+', ' ', doc_text)
        return doc_text.strip()
    ```

### Stage 3: Embedding Ingestion Pipeline
Embeddings can be generated and updated through two paths:

#### Path A: Initial Ingestion (`embed_docs.py`)
*   **Method:** `SemanticRetriever.generate_and_store_embeddings`
*   **Cypher Query:**
    ```cypher
    MATCH (d:Documentation)
    WHERE d.text IS NOT NULL AND trim(d.text) <> ''
    RETURN d.id AS id, d.text AS text
    ```
*   **Processing:** Batches results (default size: `256`) and computes embeddings directly on raw documentation texts:
    ```python
    embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    ```
*   **Write-Back:** Updates `d.embedding` directly:
    ```cypher
    UNWIND $batch AS row
    MATCH (d:Documentation {id: row.id})
    SET d.embedding = row.embedding
    ```

#### Path B: Context-Enriched Embeddings (`rebuild_embeddings.py`)
*   **File Path:** [rebuild_embeddings.py](file:///c:/Users/Dell/OneDrive/Desktop/step1/tools/rebuild_embeddings.py)
*   **Method:** `EmbeddingRebuilder.rebuild_embeddings`
*   **Cypher Query:**
    ```cypher
    MATCH (e)-[:HAS_DOC]->(d:Documentation)
    WHERE d.text IS NOT NULL AND trim(d.text) <> ''
    RETURN d.id AS doc_id, d.text AS doc_text, e.name AS name, e.signature AS signature, labels(e)[0] AS label
    ```
*   **Action:** Enhances raw documentation text with entity metadata before embedding:
    ```python
    def build_payload(label, name, signature, doc_text):
        payload = f"Entity Type: {label}\n\n"
        # Adds formatted class, method names, and signatures
        ...
        payload += f"Documentation:\n{doc_text}"
        return payload
    ```
*   **Write-Back:** Encodes this formatted payload, storing the embedding vector in `d.embedding` and the structured text payload in `d.embedding_payload`.
