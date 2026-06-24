from retriever import GraphRetriever
retriever = GraphRetriever()
res = retriever.session.run("MATCH (c:Class {name: 'SPAposition'})-[:HAS_DOCUMENTATION]->(d:Documentation) RETURN d.text LIMIT 1").data()
print("Class SPAposition doc:", res)
