import os
import time
import logging
from tqdm import tqdm
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

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
        
        search_query = """
        // 1. Vector Search
        CALL {
            MATCH (d:Documentation)
            SEARCH d IN (VECTOR INDEX documentation_embedding_index FOR $embedding LIMIT $top_k)
            SCORE AS score
            MATCH (e)-[:HAS_DOC]->(d)
            RETURN e, d, score
        }
        WITH collect({e: e, d: d, score: score}) AS vec_matches
        
        // 2. Lexical Search
        WITH vec_matches, [x IN split(toLower(trim(replace(replace($exact_query, '?', ''), '.', ''))), ' ') WHERE x <> ''] AS query_words
        WITH vec_matches, [x IN query_words WHERE NOT x IN ['what', 'is', 'how', 'does', 'work', 'are', 'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or', 'which', 'return', 'returns', 'related', 'operate', 'inherit', 'inherits', 'about', 'can', 'you', 'explain']] AS significant_words
        
        OPTIONAL MATCH (exact_e)
        WHERE (exact_e:Class OR exact_e:Method OR exact_e:Function OR exact_e:Struct OR exact_e:Enum)
          AND toLower(exact_e.name) IN significant_words
        OPTIONAL MATCH (exact_e)-[:HAS_DOC]->(exact_d:Documentation)
        
        // Group by name to prevent overloading from flooding top 10
        WITH vec_matches, exact_e.name AS ename, collect({e: exact_e, d: exact_d, score: 2.0})[0..1] AS lex_group
        UNWIND lex_group AS lex_match
        WITH vec_matches, collect(lex_match) AS lex_matches
        
        // 3. Combine
        UNWIND (vec_matches + lex_matches) AS match_record
        WITH match_record.e AS e, match_record.d AS d, match_record.score AS score
        WHERE e IS NOT NULL
        
        WITH e, labels(e)[0] AS label, max(score) AS score, head(collect(d)) AS d
        ORDER BY score DESC
        LIMIT $top_k
        
        // 4. Context Expansion
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
        
        RETURN score, label AS entity_type, coalesce(e.name, '') AS entity_name, coalesce(d.text, '') AS documentation, context
        ORDER BY score DESC
        """
        
        with self.driver.session() as session:
            records = session.run(search_query, top_k=top_k, embedding=query_embedding, exact_query=query).data()
            
        results = []
        for r in records:
            results.append({
                "score": r['score'],
                "entity_type": r['entity_type'],
                "entity_name": r['entity_name'],
                "documentation": r['documentation'],
                "context": r['context']
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
