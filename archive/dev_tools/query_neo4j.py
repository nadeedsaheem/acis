import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with driver.session() as session:
    # Get total methods without HAS_METHOD edge
    res = session.run("MATCH (m:Method) WHERE NOT ()-[:HAS_METHOD]->(m) RETURN count(m) AS count")
    print(f"Methods without HAS_METHOD: {res.single()['count']}")

    # Get a sample
    res = session.run("MATCH (m:Method) WHERE NOT ()-[:HAS_METHOD]->(m) RETURN m.id, m.name LIMIT 5")
    for record in res:
        print(f"Orphan Method: {record['m.id']} - {record['m.name']}")
        
    # Get total methods WITH HAS_METHOD edge
    res = session.run("MATCH ()-[r:HAS_METHOD]->(m:Method) RETURN count(r) AS count")
    print(f"Methods WITH HAS_METHOD: {res.single()['count']}")

driver.close()
