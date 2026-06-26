import os
import time
import logging
from tqdm import tqdm
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_payload(label, name, signature, doc_text):
    payload = f"Entity Type: {label}\n\n"
    if label == 'Method':
        # Split signature if possible or just use name
        class_part = ""
        method_part = name
        if "::" in name:
            class_part, method_part = name.split("::", 1)
        
        if class_part:
            payload += f"Class:\n{class_part}\n\n"
        payload += f"Method:\n{method_part}\n\n"
    else:
        payload += f"Entity Name: {name}\n\n"
        
    if signature:
        payload += f"Signature:\n{signature}\n\n"
        
    payload += f"Documentation:\n{doc_text}"
    return payload

class EmbeddingRebuilder:
    def __init__(self, uri, user, password, model_name="BAAI/bge-small-en-v1.5"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logging.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logging.info(f"Model loaded. Dimension: {self.dimension}")

    def close(self):
        if self.driver:
            self.driver.close()

    def rebuild_embeddings(self, batch_size=256):
        fetch_query = """
        MATCH (e)-[:HAS_DOC]->(d:Documentation)
        WHERE d.text IS NOT NULL AND trim(d.text) <> ''
        RETURN d.id AS doc_id, d.text AS doc_text, e.name AS name, e.signature AS signature, labels(e)[0] AS label
        """
        with self.driver.session() as session:
            records = session.run(fetch_query).data()
            
        total_docs = len(records)
        logging.info(f"Found {total_docs} documentation nodes to rebuild.")
        
        def store_batch_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (d:Documentation {id: row.doc_id})
            SET d.embedding = row.embedding,
                d.embedding_payload = row.payload
            """
            tx.run(query, batch=batch)
            
        success_count = 0
        failures = 0
        
        start_time = time.time()
        for i in tqdm(range(0, total_docs, batch_size), desc="Rebuilding batches"):
            batch = records[i:i+batch_size]
            texts = []
            for r in batch:
                payload = build_payload(r.get('label', ''), r.get('name', ''), r.get('signature', ''), r.get('doc_text', ''))
                texts.append(payload)
                r['payload'] = payload # Store for updating Neo4j
            
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                
                db_batch = []
                for j, r in enumerate(batch):
                    db_batch.append({
                        'doc_id': r['doc_id'],
                        'payload': r['payload'],
                        'embedding': embeddings[j].tolist()
                    })
                    
                with self.driver.session() as session:
                    session.execute_write(store_batch_tx, db_batch)
                success_count += len(batch)
            except Exception as e:
                logging.error(f"Error processing batch {i}: {e}")
                failures += len(batch)
                
        total_time = time.time() - start_time
        logging.info(f"Rebuilt {success_count} embeddings in {total_time:.2f}s")

if __name__ == "__main__":
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    rebuilder = EmbeddingRebuilder(URI, USER, PASSWORD)
    rebuilder.rebuild_embeddings()
    rebuilder.close()
