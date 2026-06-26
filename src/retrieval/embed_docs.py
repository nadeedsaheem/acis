import os
import time
import logging
from tqdm import tqdm
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from retrieval.rrf_fusion import reciprocal_rank_fusion

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SemanticRetriever:
    def __init__(self, uri, user, password, model_name="BAAI/bge-small-en-v1.5"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logging.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logging.info(f"Model loaded. Dimension: {self.dimension}")

    def close(self):
        if self.driver:
            self.driver.close()

    def generate_and_store_embeddings(self, batch_size=256):
        fetch_query = """
        MATCH (d:Documentation)
        WHERE d.text IS NOT NULL AND trim(d.text) <> ''
        RETURN d.id AS id, d.text AS text
        """
        with self.driver.session() as session:
            records = session.run(fetch_query).data()
            
        total_docs = len(records)
        logging.info(f"Found {total_docs} documentation nodes to embed.")
        
        def store_batch_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (d:Documentation {id: row.id})
            SET d.embedding = row.embedding
            """
            tx.run(query, batch=batch)
            
        success_count = 0
        failures = 0
        
        start_time = time.time()
        for i in tqdm(range(0, total_docs, batch_size), desc="Embedding batches"):
            batch = records[i:i+batch_size]
            texts = [r['text'] for r in batch]
            
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                
                db_batch = []
                for j, r in enumerate(batch):
                    db_batch.append({
                        'id': r['id'],
                        'embedding': embeddings[j].tolist()
                    })
                    
                with self.driver.session() as session:
                    session.execute_write(store_batch_tx, db_batch)
                success_count += len(batch)
            except Exception as e:
                logging.error(f"Error processing batch {i}: {e}")
                failures += len(batch)
                
        total_time = time.time() - start_time
        logging.info(f"Embedded {success_count} docs in {total_time:.2f}s")
        return success_count, failures, total_docs, total_time

    def create_vector_index(self):
        index_name = "documentation_embedding_index"
        
        check_query = "SHOW VECTOR INDEXES"
        with self.driver.session() as session:
            indexes = session.run(check_query).data()
            exists = any(idx.get('name') == index_name for idx in indexes)
            if exists:
                logging.info(f"Vector index '{index_name}' already exists. Dropping it...")
                session.run(f"DROP INDEX {index_name}")
                
            create_query = f"""
            CREATE VECTOR INDEX {index_name}
            FOR (d:Documentation)
            ON (d.embedding)
            OPTIONS {{
              indexConfig: {{
                `vector.dimensions`: {self.dimension},
                `vector.similarity_function`: 'cosine'
              }}
            }}
            """
            session.run(create_query)
            logging.info(f"Created vector index '{index_name}' with dimension {self.dimension}.")
            time.sleep(2)  # Give Neo4j a moment to populate the index

    def semantic_search(self, query, top_k=10):
        query_embedding = self.model.encode([query], normalize_embeddings=True)[0].tolist()
        
        # 1. Vector Search Query (LIMIT 50)
        vector_query = """
        MATCH (d:Documentation)
        SEARCH d IN (VECTOR INDEX documentation_embedding_index FOR $embedding LIMIT 50)
        SCORE AS score
        MATCH (e)-[:HAS_DOC]->(d)
        RETURN labels(e)[0] AS entity_type, e.id AS entity_id, coalesce(e.name, '') AS entity_name, coalesce(e.fqn, e.name, '') AS entity_fqn, coalesce(d.text, '') AS documentation, e.signature AS signature, score
        ORDER BY score DESC
        """
        
        # 2. Lexical Search Query (LIMIT 50)
        lexical_query = """
        WITH [x IN split(toLower(trim(replace(replace($exact_query, '?', ''), '.', ''))), ' ') WHERE x <> ''] AS query_words
        WITH [x IN query_words WHERE NOT x IN ['what', 'is', 'how', 'does', 'work', 'are', 'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or', 'which', 'return', 'returns', 'related', 'operate', 'inherit', 'inherits', 'about', 'can', 'you', 'explain']] AS significant_words
        
        MATCH (exact_e)
        WHERE (exact_e:Class OR exact_e:Method OR exact_e:Function OR exact_e:Struct OR exact_e:Enum)
          AND (
            toLower(exact_e.name) IN significant_words
            OR toLower(exact_e.fqn) IN significant_words
            OR any(word IN significant_words WHERE word ENDS WITH "::" + toLower(exact_e.name))
            OR any(word IN significant_words WHERE toLower(exact_e.fqn) ENDS WITH "::" + word)
          )
        OPTIONAL MATCH (exact_e)-[:HAS_DOC]->(exact_d:Documentation)
        
        // Group by name to prevent overloading from flooding top 50
        WITH exact_e.name AS ename, collect({e: exact_e, d: exact_d})[0..1] AS lex_group
        UNWIND lex_group AS lex_match
        WITH lex_match.e AS e, lex_match.d AS d
        WHERE e IS NOT NULL
        RETURN labels(e)[0] AS entity_type, e.id AS entity_id, coalesce(e.name, '') AS entity_name, coalesce(e.fqn, e.name, '') AS entity_fqn, coalesce(d.text, '') AS documentation, e.signature AS signature
        LIMIT 50
        """
        
        with self.driver.session() as session:
            vector_records = session.run(vector_query, embedding=query_embedding).data()
            lexical_records = session.run(lexical_query, exact_query=query).data()
            
        # 3. Reciprocal Rank Fusion
        fused_results = reciprocal_rank_fusion(vector_records, lexical_records, limit=top_k, k=60)
        
        if not fused_results:
            return {"query": query, "results": []}
            
        # 4. Context Expansion Query for top candidates
        candidate_ids = [item["entity_id"] for item in fused_results]
        
        context_query = """
        UNWIND $candidate_ids AS eid
        MATCH (e) WHERE (e:Class OR e:Method OR e:Function OR e:Struct OR e:Enum) AND e.id = eid
        OPTIONAL MATCH (e)-[:HAS_DOC]->(d:Documentation)
        WITH e, d, labels(e)[0] AS label
        
        CALL (e, label) {
            WITH e, label WHERE label IN ['Function', 'Method']
            OPTIONAL MATCH (e)-[:RETURNS]->(t)
            OPTIONAL MATCH (e)-[:HAS_PARAMETER]->(p:Parameter)
            WITH e, label, t, p ORDER BY p.position
            WITH e, label, t, collect(p {.name, .type, .position}) AS parameters
            OPTIONAL MATCH (c:Class)-[:HAS_METHOD]->(e)
            RETURN {
                return_type: coalesce(t.name, 'void'),
                parameters: [x IN parameters WHERE x.name IS NOT NULL],
                parent_class: coalesce(c.name, ''),
                signature: coalesce(e.signature, '')
            } AS context
            
            UNION
            
            WITH e, label WHERE label = 'Class'
            OPTIONAL MATCH (e)-[:INHERITS]->(parent)
            WITH e, label, collect(parent.name) AS parents
            OPTIONAL MATCH (e)-[:HAS_METHOD]->(m:Method)
            WITH e, label, parents, collect(m.name) AS methods
            RETURN {
                parents: [x IN parents WHERE x IS NOT NULL],
                methods: [x IN methods WHERE x IS NOT NULL]
            } AS context
            
            UNION
            
            WITH e, label WHERE label IN ['Struct', 'Enum']
            RETURN {} AS context
        }
        
        RETURN e.id AS entity_id, coalesce(d.text, '') AS documentation, context
        """
        
        with self.driver.session() as session:
            context_records = session.run(context_query, candidate_ids=candidate_ids).data()
            
        # Map context records by entity_id
        context_map = {r["entity_id"]: r for r in context_records}
        
        # 5. Assemble final response
        results = []
        for item in fused_results:
            entity_id = item["entity_id"]
            ctx_data = context_map.get(entity_id, {"documentation": item.get("documentation", ""), "context": {}})
            
            results.append({
                "score": item["score"],
                "entity_type": item["entity_type"],
                "entity_id": entity_id,
                "entity_name": item["entity_name"],
                "fqn": item["fqn"],
                "documentation": ctx_data.get("documentation") or item.get("documentation", ""),
                "context": ctx_data.get("context", {})
            })
            
        return {
            "query": query,
            "results": results
        }

    def verify_embeddings(self):
        query = """
        MATCH (d:Documentation)
        RETURN count(d) AS total,
               sum(CASE WHEN d.embedding IS NOT NULL THEN 1 ELSE 0 END) AS embedded
        """
        with self.driver.session() as session:
            res = session.run(query).data()[0]
        return res['total'], res['embedded']

def execute_phase7b():
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    retriever = SemanticRetriever(URI, USER, PASSWORD)
    
    # Check if we need to embed
    total_db, embedded_db = retriever.verify_embeddings()
    if total_db == embedded_db and total_db > 0:
        logging.info("All documentation nodes are already embedded. Skipping generation.")
        success_count = embedded_db
        failures = 0
        total_docs = total_db
        embed_time = 0.0
    else:
        # 1. Embed Docs
        success_count, failures, total_docs, embed_time = retriever.generate_and_store_embeddings()
    
    # 2. Create Vector Index
    try:
        retriever.create_vector_index()
        index_created = True
    except Exception as e:
        logging.error(f"Failed to create vector index: {e}")
        index_created = False

    # 3. Verify
    total_db, embedded_db = retriever.verify_embeddings()
    
    # 4. Semantic Search Tests
    test_queries = [
        "How are smooth edge transitions generated?",
        "How does variable radius blending work?",
        "Functions that return outcome",
        "Methods related to SPAposition",
        "Entity journaling operations"
    ]
    
    # Warmup
    logging.info("Running warmup query to initialize model and Neo4j index...")
    try:
        retriever.semantic_search("warmup query", top_k=1)
    except Exception as e:
        pass
    
    query_results = []
    total_query_time = 0
    search_passed = True
    
    for q in test_queries:
        try:
            start_q = time.time()
            res = retriever.semantic_search(q, top_k=10)
            q_time = time.time() - start_q
            total_query_time += q_time
            
            nodes_found = len(res.get('results', []))
            if nodes_found == 0:
                search_passed = False
                
            query_results.append({
                "query": q,
                "time": q_time,
                "nodes": nodes_found,
                "results": res['results']
            })
        except Exception as e:
            logging.error(f"Query '{q}' failed: {e}")
            search_passed = False
            query_results.append({
                "query": q,
                "time": 0,
                "nodes": 0,
                "error": str(e)
            })
            
    avg_query_time = total_query_time / len(test_queries) if test_queries else 0
    
    # Write Validation Report
    report = "# ACIS Knowledge Graph Phase 7B - Validation Report\n\n"
    report += "## Embedding Generation\n"
    report += f"- **Total Documentation Nodes in DB:** {total_db}\n"
    report += f"- **Documentation Nodes Embedded:** {embedded_db}\n"
    report += f"- **Embedding Dimension:** {retriever.dimension}\n"
    report += f"- **Embedding Generation Time:** {embed_time:.2f} seconds\n"
    report += f"- **Skipped Nodes (empty/null):** {total_db - total_docs}\n"
    report += f"- **Embedding Failures:** {failures}\n\n"
    
    report += "## Vector Index\n"
    report += f"- **Vector Index Created:** {'Yes' if index_created else 'No'}\n\n"
    
    report += "## Semantic Search Tests\n"
    report += f"- **Average Query Time:** {avg_query_time:.3f} seconds\n\n"
    
    for r in query_results:
        report += f"### Query: `{r['query']}`\n"
        if 'error' in r:
            report += f"- **ERROR:** {r['error']}\n"
        else:
            report += f"- **Execution Time:** {r['time']:.3f} seconds\n"
            report += f"- **Retrieved Nodes:** {r['nodes']}\n"
            if r['nodes'] > 0:
                report += "- **Top 3 Results:**\n"
                for idx, res in enumerate(r['results'][:3]):
                    report += f"  {idx+1}. `[{res['entity_type']}] {res['entity_name']}` (Score: {res['score']:.4f})\n"
        report += "\n"
        
    with open('phase7b_validation_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    # Write Certification Report
    cert = "# Phase 7B Certification\n\n"
    
    passed = True
    reasons = []
    
    if embedded_db != total_db:
        # Wait, if total_db is empty/null, they were skipped. 
        # Actually total_db counts all Documentation nodes. If they are empty/null they won't be embedded.
        # But we filtered empty/null in parse? Yes, "filtered out empty, null"
        # So total_db should exactly equal total_docs and embedded_db!
        if total_db != embedded_db:
            passed = False
            reasons.append(f"Mismatch: Embedded ({embedded_db}) != Total DB ({total_db})")
            
    if embedded_db == 0:
        passed = False
        reasons.append("No documentation nodes embedded.")
        
    if failures > 0:
        passed = False
        reasons.append(f"Embedding failures detected: {failures}")
        
    if not index_created:
        passed = False
        reasons.append("Vector Index creation failed.")
        
    if not search_passed:
        passed = False
        reasons.append("One or more validation queries failed or returned 0 results.")
        
    if avg_query_time >= 2.0:
        passed = False
        reasons.append(f"Average query time ({avg_query_time:.3f}s) >= 2.0s")
        
    if passed:
        cert += "## Status: PASSED\n\n"
        cert += "All certification checks passed successfully.\n\n"
    else:
        cert += "## Status: FAILED\n\n"
        cert += "The following checks failed:\n"
        for r in reasons:
            cert += f"- {r}\n"
            
    cert += "### Metrics:\n"
    cert += f"- Embedded Nodes: {embedded_db} / {total_db}\n"
    cert += f"- Vector Index: {'Active' if index_created else 'Missing'}\n"
    cert += f"- Average Query Time: {avg_query_time:.3f} seconds\n"
    
    with open('phase7b_certification.md', 'w', encoding='utf-8') as f:
        f.write(cert)
        
    retriever.close()

if __name__ == '__main__':
    execute_phase7b()
