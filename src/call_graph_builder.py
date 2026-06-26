import os
import json
import logging
import hashlib
import time
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

class CallGraphBuilder:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logging.info("Connected to Neo4j successfully for call graph builder.")
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def load_calls(self, data):
        if not self.driver:
            logging.error("No active Neo4j driver connection.")
            return False

        # 1. Fetch all existing Function and Method nodes to build a resolution map in memory
        logging.info("Fetching existing function and method nodes from Neo4j...")
        name_to_fqns = {}
        fqn_exists = set()
        
        query = """
        MATCH (n)
        WHERE n:Function OR n:Method
        RETURN n.name AS name, n.fqn AS fqn
        """
        
        try:
            with self.driver.session() as session:
                records = session.run(query).data()
                for r in records:
                    name = r['name']
                    fqn = r['fqn']
                    if fqn:
                        fqn_exists.add(fqn)
                        if name not in name_to_fqns:
                            name_to_fqns[name] = []
                        if fqn not in name_to_fqns[name]:
                            name_to_fqns[name].append(fqn)
            logging.info(f"Loaded {len(fqn_exists)} existing symbol FQNs in memory.")
        except Exception as e:
            logging.error(f"Error fetching symbols: {e}")
            return False

        # 2. Process and resolve all calls
        all_calls = []
        for file_record in data:
            for call in file_record.get("calls", []):
                all_calls.append(call)

        logging.info(f"Processing {len(all_calls)} function call invocations...")
        
        resolved_links = []
        external_functions = {}
        
        for call in all_calls:
            caller = call.get("caller")
            callee_name = call.get("callee_name")
            callee_fqn_guess = call.get("callee_fqn")
            line = call.get("line", 0)
            
            if not caller or not callee_name:
                continue
                
            resolved_callee_fqn = None
            
            # Step A: Check if guess FQN exists
            if callee_fqn_guess in fqn_exists:
                resolved_callee_fqn = callee_fqn_guess
            # Step B: Check if name matches any candidate FQNs
            elif callee_name in name_to_fqns:
                candidates = name_to_fqns[callee_name]
                if len(candidates) == 1:
                    resolved_callee_fqn = candidates[0]
                else:
                    # Rank by namespace overlap with caller
                    caller_parts = caller.split("::")
                    best_cand = candidates[0]
                    best_overlap = -1
                    for cand in candidates:
                        cand_parts = cand.split("::")
                        overlap = 0
                        for cp, sp in zip(cand_parts[:-1], caller_parts[:-1]):
                            if cp == sp:
                                overlap += 1
                            else:
                                break
                        if overlap > best_overlap:
                            best_overlap = overlap
                            best_cand = cand
                    resolved_callee_fqn = best_cand
            
            # Step C: External function fallback
            if not resolved_callee_fqn:
                # Use the guess or prefix it with std if applicable
                resolved_callee_fqn = callee_fqn_guess
                if resolved_callee_fqn.startswith("unresolved::"):
                    resolved_callee_fqn = resolved_callee_fqn.replace("unresolved::", "")
                
                # Check for standard namespace or keep as is
                if resolved_callee_fqn not in external_functions:
                    external_functions[resolved_callee_fqn] = {
                        "fqn": resolved_callee_fqn,
                        "name": callee_name,
                        "id": generate_hash(resolved_callee_fqn)
                    }
                    
            resolved_links.append({
                "caller_fqn": caller,
                "callee_fqn": resolved_callee_fqn or callee_fqn_guess,
                "line": line
            })

        # 3. Create unique constraint for ExternalFunction if not exists
        try:
            with self.driver.session() as session:
                session.run("CREATE CONSTRAINT external_function_fqn_unique IF NOT EXISTS FOR (e:ExternalFunction) REQUIRE e.fqn IS UNIQUE")
        except Exception as e:
            logging.warning(f"Could not create constraint for ExternalFunction: {e}")

        # 4. Batch Ingest External Functions
        if external_functions:
            logging.info(f"Ingesting {len(external_functions)} ExternalFunction nodes...")
            ext_list = list(external_functions.values())
            ext_query = """
            UNWIND $batch AS row
            MERGE (e:ExternalFunction {fqn: row.fqn})
            ON CREATE SET e.name = row.name, e.is_external = true, e.id = row.id
            """
            try:
                with self.driver.session() as session:
                    session.run(ext_query, batch=ext_list)
            except Exception as e:
                logging.error(f"Error ingesting external functions: {e}")
                return False

        # 5. Batch Ingest CALLS / CALLED_BY relationships
        if resolved_links:
            logging.info(f"Ingesting {len(resolved_links)} CALLS & CALLED_BY relationships...")
            
            # Batch size optimization
            batch_size = 2000
            for i in range(0, len(resolved_links), batch_size):
                batch = resolved_links[i:i+batch_size]
                link_query = """
                UNWIND $batch AS row
                MATCH (caller) WHERE (caller:Function OR caller:Method) AND caller.fqn = row.caller_fqn
                MATCH (callee) WHERE (callee:Function OR callee:Method OR callee:ExternalFunction) AND callee.fqn = row.callee_fqn
                MERGE (caller)-[r:CALLS {line: row.line}]->(callee)
                MERGE (callee)-[r2:CALLED_BY {line: row.line}]->(caller)
                """
                try:
                    with self.driver.session() as session:
                        session.run(link_query, batch=batch)
                except Exception as e:
                    logging.error(f"Error ingesting calls batch starting at {i}: {e}")
                    return False
                    
        logging.info("Call Graph Builder completed successfully.")
        return True

if __name__ == '__main__':
    logging.info("Starting Call Graph Builder CLI...")
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    # Check if code_base.json exists
    json_path = 'code_base.json'
    if not os.path.exists(json_path):
        json_path = 'data/code_base.json'
        
    if not os.path.exists(json_path):
        logging.error(f"Could not find code_base.json at root or data/ directories.")
    else:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        builder = CallGraphBuilder(URI, USER, PASSWORD)
        builder.load_calls(data)
        builder.close()
