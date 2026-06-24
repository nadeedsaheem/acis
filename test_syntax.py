import neo4j
driver = neo4j.GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'nadeed@3973'))
with driver.session() as session:
    emb = [0.1] * 384
    
    q1 = '''CALL db.index.vector.queryNodes('documentation_embedding_index', 1, $emb) YIELD node, score RETURN score'''
    try:
        res = session.run(q1, emb=emb).data()
        print('OLD', res)
    except Exception as e: print('Error on OLD:', e)
    
    q3 = '''MATCH (d:Documentation)
            SEARCH d IN (VECTOR INDEX documentation_embedding_index FOR $emb LIMIT 1)
            SCORE AS score
            RETURN score'''
    try:
        res = session.run(q3, emb=emb).data()
        print('SEARCH', res)
    except Exception as e: print('Error on SEARCH:', e)
