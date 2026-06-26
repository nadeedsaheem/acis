import neo4j
driver = neo4j.GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'nadeed@3973'))
with driver.session() as session:
    emb = [0.1] * 384
    q = '''
        MATCH (d:Documentation)
        SEARCH d IN (VECTOR INDEX documentation_embedding_index FOR $emb LIMIT 1)
        SCORE AS score
        MATCH (e)-[:HAS_DOC]->(d)
        WITH d, score, e, labels(e)[0] AS label
        CALL (e, label) {
            WITH e, label WHERE label IN ['Function', 'Method']
            RETURN 1 AS context
            UNION
            WITH e, label WHERE label = 'Class'
            RETURN 2 AS context
            UNION
            WITH e, label WHERE label IN ['Struct', 'Enum']
            RETURN 3 AS context
        }
        RETURN score, label, context
    '''
    try:
        res = session.run(q, emb=emb).data()
        print('SUCCESS', res)
    except Exception as e: print('Error:', e)
