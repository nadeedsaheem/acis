from neo4j import GraphDatabase
import time

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'nadeed@3973'))

# Wait for index to be online
for attempt in range(30):
    with driver.session() as s:
        res = s.run("SHOW INDEXES YIELD name, state, populationPercent WHERE name = 'documentation_embedding_index'").data()
    if res:
        print(f"Index state: {res[0]['state']}, Population: {res[0]['populationPercent']}%")
        if res[0]['state'] == 'ONLINE' and res[0]['populationPercent'] == 100.0:
            break
    else:
        print("Index not found yet...")
    time.sleep(3)

# Also print DB stats
with driver.session() as s:
    labels = ['File', 'Class', 'Method', 'Function', 'Struct', 'Enum', 'Documentation']
    for label in labels:
        count = s.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()['c']
        print(f"{label}: {count}")
    
    embedded = s.run("MATCH (d:Documentation) WHERE d.embedding IS NOT NULL RETURN count(d) AS c").single()['c']
    print(f"Docs with embeddings: {embedded}")

driver.close()
print("Done!")
