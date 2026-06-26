"""
Script to rebuild the Neo4j graph from the current code_base.json.
This ensures all entities (including File nodes, SPAposition, Functions)
are correctly loaded with paths matching the current JSON schema.
"""
import os
import sys

# Add src/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from build_graph import KnowledgeGraphBuilder, generate_report

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'code_base.json')

print(f"Connecting to Neo4j at {URI}...")
builder = KnowledgeGraphBuilder(URI, USER, PASSWORD)
if builder.driver:
    print("Resetting database...")
    builder.reset_database()
    
    print("Creating identity constraints...")
    builder.create_constraints()
    
    print(f"Loading JSON data from {JSON_PATH}...")
    data = builder.load_data(JSON_PATH)
    if data:
        print(f"Loaded {len(data)} records. Starting graph build...")
        stats = builder.build_graph(data)
        print("Graph build complete. Validating...")
        validation = builder.validate_graph()
        generate_report(stats, validation)
        print("\n=== Build Summary ===")
        print(f"Files loaded:   {stats.get('files_loaded', 0)}")
        print(f"Classes loaded: {stats.get('classes_loaded', 0)}")
        print(f"Methods loaded: {stats.get('methods_loaded', 0)}")
        print(f"Functions loaded: {stats.get('functions_loaded', 0)}")
        print(f"Enums loaded:   {stats.get('enums_loaded', 0)}")
        print(f"Structs loaded: {stats.get('structs_loaded', 0)}")
        print(f"Docs loaded:    {stats.get('docs_loaded', 0)}")
        print(f"Failures:       {stats.get('failures', 0)}")
    builder.close()
else:
    print("ERROR: Failed to connect to Neo4j.")
