import os
import json
import time
import logging
import re
from neo4j import GraphDatabase

__all__ = ["KnowledgeGraphRetriever", "semantic_search", "validate_retrieval"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

_semantic_retriever_instance = None

def semantic_search(query, top_k=10):
    """
    Top-level importable function for vector semantic search.
    Implements a lazy-loading singleton to prevent reloading the embedding model on every call.
    """
    global _semantic_retriever_instance
    if _semantic_retriever_instance is None:
        try:
            from retrieval.embed_docs import SemanticRetriever
        except ImportError:
            raise ImportError("Could not import SemanticRetriever from embed_docs.py")
            
        URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        USER = os.getenv("NEO4J_USER", "neo4j")
        PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
        
        _semantic_retriever_instance = SemanticRetriever(URI, USER, PASSWORD)
        
    return _semantic_retriever_instance.semantic_search(query, top_k=top_k)

class KnowledgeGraphRetriever:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def search(self, query, top_k=10):
        query_lower = query.lower()
        keywords = query_lower.split()
        
        results_map = {}
        
        def add_or_update_score(node_id, entity_type, score_increment, node_data):
            if node_id not in results_map:
                results_map[node_id] = {
                    'entity_type': entity_type,
                    'score': 0,
                    'data': node_data
                }
            results_map[node_id]['score'] += score_increment
        kw_conditions_doc = []
        kw_conditions_name = []
        kw_conditions_sig = []
        params = {"exact_query": query_lower}
        for i, kw in enumerate(keywords):
            params[f"kw_{i}"] = kw
            kw_conditions_doc.append(f"ltext CONTAINS $kw_{i}")
            kw_conditions_name.append(f"lname CONTAINS $kw_{i}")
            kw_conditions_sig.append(f"lsig CONTAINS $kw_{i}")
            
        doc_where = " OR ".join(kw_conditions_doc) if kw_conditions_doc else "false"
        name_where = " OR ".join(kw_conditions_name) if kw_conditions_name else "false"
        sig_where = " OR ".join(kw_conditions_sig) if kw_conditions_sig else "false"

        with self.driver.session() as session:
            # 1. Documentation Match
            doc_query = f"""
            MATCH (d:Documentation)
            WITH d, toLower(d.text) AS ltext
            WHERE ltext CONTAINS $exact_query OR {doc_where}
            MATCH (e)-[:HAS_DOC]->(d)
            RETURN e.id AS id, labels(e)[0] AS label, d.text AS doc_text, e, 
                   CASE WHEN ltext CONTAINS $exact_query THEN true ELSE false END AS is_exact
            """
            
            t0 = time.time()
            doc_records = session.run(doc_query, **params)
            for r in doc_records:
                score = 10  # Documentation Match
                if r['is_exact']:
                    score += 15 # Exact Match
                else:
                    score += 5  # Partial Match
                
                entity = r['e']
                add_or_update_score(r['id'], r['label'], score, {
                    'node': dict(entity),
                    'doc_text': r['doc_text']
                })
            t1 = time.time()
            logging.info(f"Doc query took {t1 - t0:.3f}s")

            # 2. Entity Name/Signature/FQN Match
            entity_query = f"""
            MATCH (e)
            WHERE e:Function OR e:Method OR e:Class OR e:Struct OR e:Enum
            WITH e, toLower(e.name) AS lname, toLower(e.signature) AS lsig, coalesce(toLower(e.fqn), '') AS lfqn
            WHERE (lname CONTAINS $exact_query OR lsig CONTAINS $exact_query OR lfqn CONTAINS $exact_query) 
               OR {name_where} OR {sig_where}
            OPTIONAL MATCH (e)-[:HAS_DOC]->(d:Documentation)
            RETURN e.id AS id, labels(e)[0] AS label, e, d.text AS doc_text, 
                   CASE WHEN (lname CONTAINS $exact_query OR lsig CONTAINS $exact_query OR lfqn CONTAINS $exact_query) THEN true ELSE false END AS is_exact
            """
            
            t2 = time.time()
            entity_records = session.run(entity_query, **params)
            for r in entity_records:
                score = 8  # Name Match
                if r['is_exact']:
                    score += 15 # Exact Match
                else:
                    score += 5  # Partial Match
                    
                entity = r['e']
                fqn = entity.get('fqn', '')
                if fqn:
                    fqn_lower = fqn.lower()
                    if fqn_lower == query_lower:
                        score += 30  # Exact FQN Match
                    elif fqn_lower.endswith("::" + query_lower):
                        score += 25  # Name matching FQN suffix
                    elif query_lower in fqn_lower:
                        score += 10  # Partial FQN Match

                add_or_update_score(r['id'], r['label'], score, {
                    'node': dict(entity),
                    'doc_text': r['doc_text'] if r['doc_text'] is not None else ''
                })
            t3 = time.time()
            logging.info(f"Entity query took {t3 - t2:.3f}s")
                
            # Sort by score
            t4 = time.time()
            sorted_candidates = sorted(results_map.values(), key=lambda x: x['score'], reverse=True)[:top_k]
            
            final_results = []
            for candidate in sorted_candidates:
                node = candidate['data']['node']
                label = candidate['entity_type']
                node_id = node.get('id')
                doc_text = candidate['data'].get('doc_text', '')
                
                result_obj = {
                    "entity_type": label,
                    "entity_id": node_id,
                    "name": node.get('name', ''),
                    "fqn": node.get('fqn', ''),
                    "score": candidate['score'],
                    "documentation": doc_text
                }
                
                # Context Expansion
                if label in ['Function', 'Method']:
                    result_obj['signature'] = node.get('signature', '')
                    
                    ctx_query = f"""
                    MATCH (n:{label} {{id: $node_id}})
                    OPTIONAL MATCH (n)-[:RETURNS]->(t)
                    OPTIONAL MATCH (n)-[:HAS_PARAMETER]->(p:Parameter)
                    WITH n, t, p ORDER BY p.position
                    WITH n, t, collect(p {{.name, .type, .position, .default_value}}) AS parameters
                    OPTIONAL MATCH (c:Class)-[:HAS_METHOD]->(n)
                    RETURN t.name AS type_name, labels(t)[0] AS type_label,
                           parameters,
                           c.name AS class_name
                    """
                    ctx_res = session.run(ctx_query, node_id=node_id).data()
                    
                    if ctx_res:
                        row = ctx_res[0]
                        result_obj['return_type'] = row.get('type_name') if row.get('type_name') else 'void'
                        
                        params = row.get('parameters', [])
                        # Filter out empty dicts from OPTIONAL MATCH
                        result_obj['parameters'] = [p for p in params if p and p.get('name') is not None]
                        
                        if label == 'Method' and row.get('class_name'):
                            result_obj['parent_class'] = row.get('class_name')
                    else:
                        result_obj['return_type'] = 'void'
                        result_obj['parameters'] = []
                        
                elif label == 'Enum':
                    enum_query = """
                    MATCH (e:Enum {id: $node_id})-[:HAS_VALUE]->(v:EnumValue)
                    RETURN v.name AS name, v.position AS position
                    ORDER BY v.position
                    """
                    vals = session.run(enum_query, node_id=node_id).data()
                    result_obj['values'] = [v.get('name') for v in vals]

                final_results.append(result_obj)
            t5 = time.time()
            logging.info(f"Context expansion took {t5 - t4:.3f}s")
                
        return {
            "query": query,
            "results": final_results
        }

def validate_retrieval(retriever):
    queries = [
        "blend",
        "outcome",
        "ENTITY",
        "SPAposition",
        "variable radius"
    ]
    
    report = "# ACIS Knowledge Graph Phase 7A - Retrieval Validation Report\n\n"
    report += "## Neo4j Connection Status\n"
    
    try:
        retriever.driver.verify_connectivity()
        report += "- **Status:** SUCCESS (Connected to Neo4j)\n\n"
        connection_success = True
    except Exception as e:
        report += f"- **Status:** FAILED ({e})\n\n"
        connection_success = False

    report += "## Search Queries Validation\n\n"
    
    certification = {
        "connected": connection_success,
        "results_found": True,
        "no_crashes": True,
        "no_orphans": True,
        "total_time": 0,
        "avg_time": 0,
        "queries_tested": len(queries)
    }
    
    if connection_success:
        total_time = 0
        
        for q in queries:
            try:
                start = time.time()
                res = retriever.search(q, top_k=10)
                duration = time.time() - start
                
                total_time += duration
                
                results = res.get('results', [])
                if not results:
                    certification["results_found"] = False
                
                report += f"### Query: `{q}`\n"
                report += f"- **Execution Time:** {duration:.3f} seconds\n"
                report += f"- **Results Found:** {len(results)}\n"
                
                entity_types = {}
                for r in results:
                    et = r.get('entity_type', 'Unknown')
                    entity_types[et] = entity_types.get(et, 0) + 1
                    
                    if et in ['Function', 'Method'] and 'return_type' not in r:
                        certification["no_orphans"] = False
                
                report += "- **Returned Entity Types:**\n"
                for et, count in entity_types.items():
                    report += f"  - {et}: {count}\n"
                    
                report += "\n"
                
            except Exception as e:
                certification["no_crashes"] = False
                report += f"### Query: `{q}`\n"
                report += f"- **CRASHED:** {e}\n\n"
                logging.error(f"Crash on query '{q}': {e}")
                
        certification["total_time"] = total_time
        certification["avg_time"] = total_time / len(queries) if len(queries) > 0 else 0
    
    with open('retrieval_validation_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    logging.info("Generated retrieval_validation_report.md")
        
    cert_report = "# Phase 7A Certification\n\n"
    
    passed = True
    reasons = []
    
    if not certification["connected"]:
        passed = False
        reasons.append("Neo4j connection failed")
    if not certification["results_found"]:
        passed = False
        reasons.append("One or more test queries returned 0 results")
    if not certification["no_crashes"]:
        passed = False
        reasons.append("One or more queries caused a crash")
    if not certification["no_orphans"]:
        passed = False
        reasons.append("Orphan expansions detected (missing critical context fields)")
    if certification["avg_time"] >= 2.0:
        passed = False
        reasons.append(f"Average retrieval time ({certification['avg_time']:.2f}s) >= 2.0s")
        
    if passed:
        cert_report += "## Status: PASSED\n\n"
        cert_report += "All certification checks passed successfully.\n\n"
    else:
        cert_report += "## Status: FAILED\n\n"
        cert_report += "The following checks failed:\n"
        for r in reasons:
            cert_report += f"- {r}\n"
            
    cert_report += "### Metrics:\n"
    cert_report += f"- Connection: {'OK' if certification['connected'] else 'FAIL'}\n"
    cert_report += f"- Avg Retrieval Time: {certification['avg_time']:.3f} seconds\n"
    cert_report += f"- Queries Tested: {certification['queries_tested']}\n"
    
    with open('retrieval_certification.md', 'w', encoding='utf-8') as f:
        f.write(cert_report)
    logging.info("Generated retrieval_certification.md")

if __name__ == '__main__':
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    retriever = KnowledgeGraphRetriever(URI, USER, PASSWORD)
    validate_retrieval(retriever)
    retriever.close()
