import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def check_db():
    with driver.session() as session:
        # Check Function IDs vs Parameter parent_ids
        print("Checking a sample parameter...")
        result = session.run("""
        MATCH (p:Parameter)
        RETURN p.id LIMIT 1
        """)
        for r in result:
            print(f"Sample Parameter ID: {r['p.id']}")
        
        # Check why HAS_PARAMETER failed
        # Since I didn't store parent_id on the Parameter node itself, I can't check it from DB.
        # But I can check if Function nodes exist.
        f_count = session.run("MATCH (f:Function) RETURN count(f) AS c").single()['c']
        print(f"Total Functions: {f_count}")
        
        m_count = session.run("MATCH (m:Method) RETURN count(m) AS c").single()['c']
        print(f"Total Methods: {m_count}")
        
        c_count = session.run("MATCH (c:Class) RETURN count(c) AS c").single()['c']
        print(f"Total Classes: {c_count}")
        
        p_count = session.run("MATCH (p:Parameter) RETURN count(p) AS c").single()['c']
        print(f"Total Parameters: {p_count}")

check_db()
driver.close()
