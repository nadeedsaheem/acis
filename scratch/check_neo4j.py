import os
from neo4j import GraphDatabase

def main():
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # Count all key entities
        labels = ['File', 'Class', 'Method', 'Function', 'Struct', 'Enum', 'Documentation']
        for label in labels:
            count = session.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()['c']
            print(f"{label}: {count}")

        print()
        # Check if any classes have the CONTAINS relationship from File
        contains = session.run("MATCH ()-[r:CONTAINS]->() RETURN count(r) AS c").single()['c']
        print(f"CONTAINS edges: {contains}")
        
        # Check has_doc edges
        has_doc = session.run("MATCH ()-[r:HAS_DOC]->() RETURN count(r) AS c").single()['c']
        print(f"HAS_DOC edges: {has_doc}")
        
        has_method = session.run("MATCH ()-[r:HAS_METHOD]->() RETURN count(r) AS c").single()['c']
        print(f"HAS_METHOD edges: {has_method}")
        
        # Sample 3 class nodes
        print()
        print("=== Sample 3 Class Nodes ===")
        res = session.run("MATCH (c:Class) RETURN c.id, c.name LIMIT 3")
        for r in res:
            print(f"  id={r['c.id']}, name={r['c.name']}")

    driver.close()

if __name__ == '__main__':
    main()
