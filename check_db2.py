import os
import json
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def check_db():
    with driver.session() as session:
        # Pick 1 Parameter
        result = session.run("MATCH (p:Parameter) RETURN p.id LIMIT 1")
        pid = result.single()['p.id']
        print(f"Testing Parameter ID: {pid}")

        # Let's find its parent_id from JSON (we can't from graph, so let's parse a bit)
        with open('code_base.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        import hashlib
        def h(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
        
        found_p = None
        found_parent = None
        for item in data:
            path = item.get('path', '')
            for fn in item.get('functions', []):
                name = fn.get('name')
                params = fn.get('parameters', [])
                param_str = ", ".join(p.get('type', '') for p in params)
                signature = f"{name}({param_str})"
                ln = fn.get('line_number', 0)
                parent_id = h(f"{path}::{name}::{signature}::{ln}")
                for pos, p in enumerate(params):
                    p_name = p.get('name', '')
                    p_type = p.get('type', '')
                    p_id = h(f"{parent_id}::param::{pos}::{p_name}::{p_type}")
                    if p_id == pid:
                        found_p = p
                        found_parent = parent_id
                        break
                if found_p: break
            if found_p: break
        
        print(f"Found parent_id in JSON: {found_parent}")
        if found_parent:
            # Does this parent exist in DB?
            f_node = session.run("MATCH (f:Function {id: $pid}) RETURN f.id", pid=found_parent).single()
            m_node = session.run("MATCH (m:Method {id: $pid}) RETURN m.id", pid=found_parent).single()
            print(f"Matches Function? {bool(f_node)}")
            print(f"Matches Method? {bool(m_node)}")

        # Run the HAS_PARAMETER query exactly as it is in build_graph.py
        print("Testing HAS_PARAMETER query...")
        query = """
        MATCH (p:Parameter {id: $p_id})
        OPTIONAL MATCH (fn:Function {id: $parent_id})
        OPTIONAL MATCH (m:Method {id: $parent_id})
        WITH p, coalesce(fn, m) AS parent
        RETURN parent IS NOT NULL AS has_parent
        """
        res = session.run(query, p_id=pid, parent_id=found_parent).single()
        print(f"Query Result has_parent: {res['has_parent'] if res else None}")

        # Check USES_TYPE count again
        ut_count = session.run("MATCH (:Parameter)-[r:USES_TYPE]->(:Class) RETURN count(r) AS c").single()['c']
        hp_count = session.run("MATCH ()-[r:HAS_PARAMETER]->(:Parameter) RETURN count(r) AS c").single()['c']
        print(f"DB USES_TYPE edges: {ut_count}")
        print(f"DB HAS_PARAMETER edges: {hp_count}")

check_db()
driver.close()
