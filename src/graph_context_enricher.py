import os
import time
from neo4j import GraphDatabase

class GraphContextEnricher:
    def __init__(self):
        URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        USER = os.getenv("NEO4J_USER", "neo4j")
        PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def close(self):
        self.driver.close()

    def enrich(self, results):
        if not results: return []
        
        # Prepare batch input
        entities = []
        for r in results:
            name = r.get("name") or r.get("entity_name") or ""
            entities.append({
                "entity_type": r.get("entity_type", "Entity"),
                "entity_id": r.get("entity_id", ""),
                "name": name
            })
            
        cypher = """
        UNWIND $entities AS e
        MATCH (n) WHERE (e.entity_id <> "" AND n.id = e.entity_id) OR (e.entity_id = "" AND labels(n)[0] = e.entity_type AND n.name = e.name)
        
        CALL (n) {
            OPTIONAL MATCH (child)-[:INHERITS]->(n)
            RETURN collect(child.name) AS child_classes
        }
        CALL (n) {
            OPTIONAL MATCH (n)-[:INHERITS]->(parent)
            RETURN collect(parent.name) AS parent_classes
        }
        CALL (n) {
            OPTIONAL MATCH (n)-[:HAS_METHOD]->(m)
            RETURN collect(m.name) AS methods
        }
        CALL (n) {
            OPTIONAL MATCH (func)-[:RETURNS]->(n)
            RETURN collect(func.name) AS returned_by
        }
        CALL (n) {
            OPTIONAL MATCH (func)-[:HAS_PARAMETER]->(p:Parameter) WHERE p.type = n.name
            RETURN collect(func.name) AS used_as_parameter
        }
        CALL (n) {
            OPTIONAL MATCH (n)-[:RETURNS]->(ret)
            RETURN collect(ret.name) AS returns_types
        }
        CALL (n) {
            OPTIONAL MATCH (c)-[:HAS_METHOD]->(n)
            RETURN collect(c.name) AS owning_classes
        }
        CALL (n) {
            OPTIONAL MATCH (n)-[:HAS_VALUE]->(v)
            RETURN collect(v.name) AS enum_values
        }
        
        RETURN e.name AS name, e.entity_type AS entity_type,
               child_classes, parent_classes, methods, returned_by, 
               used_as_parameter, returns_types, owning_classes, enum_values
        """
        
        enrichment_map = {}
        try:
            with self.driver.session() as session:
                records = session.run(cypher, entities=entities)
                for r in records:
                    key = f"{r['entity_type']}::{r['name']}"
                    
                    # Clean up empty strings or nulls from collections
                    def clean(lst):
                        return [x for x in lst if x]
                        
                    enrichment_map[key] = {
                        "child_classes": clean(r.get("child_classes", [])),
                        "parent_classes": clean(r.get("parent_classes", [])),
                        "methods": clean(r.get("methods", [])),
                        "returned_by": clean(r.get("returned_by", [])),
                        "used_as_parameter": clean(r.get("used_as_parameter", [])),
                        "returns": clean(r.get("returns_types", [])),
                        "owning_class": clean(r.get("owning_classes", [])),
                        "enum_values": clean(r.get("enum_values", []))
                    }
        except Exception as e:
            print(f"Error enriching context: {e}")
            
        # Merge back into results
        enriched_results = []
        for r in results:
            name = r.get("name") or r.get("entity_name") or ""
            key = f"{r.get('entity_type')}::{name}"
            rels = enrichment_map.get(key, {})
            
            # Map into the expected structure
            new_r = {
                "entity": {
                    "type": r.get("entity_type", "Entity"),
                    "name": name
                },
                "documentation": r.get("documentation", ""),
                "relationships": {}
            }
            
            # Populate relationships dynamically
            if rels.get("parent_classes"): new_r["relationships"]["inherits"] = rels["parent_classes"]
            if rels.get("child_classes"): new_r["relationships"]["inherited_by"] = rels["child_classes"]
            if rels.get("methods"): new_r["relationships"]["methods"] = rels["methods"]
            if rels.get("returned_by"): new_r["relationships"]["returned_by"] = rels["returned_by"]
            if rels.get("used_as_parameter"): new_r["relationships"]["used_as_parameter"] = rels["used_as_parameter"]
            if rels.get("returns"): new_r["relationships"]["returns"] = rels["returns"]
            if rels.get("owning_class"): new_r["relationships"]["owning_class"] = rels["owning_class"]
            if rels.get("enum_values"): new_r["relationships"]["enum_values"] = rels["enum_values"]
            
            # Include old params if present
            if r.get("parameters"):
                # old params were dicts
                new_r["relationships"]["parameters"] = [p.get('name') for p in r['parameters'] if isinstance(p, dict)]
                
            enriched_results.append(new_r)
            
        return enriched_results

# Expose a singleton-like enricher
_enricher_instance = None

def enrich_context(results: list) -> list:
    global _enricher_instance
    if _enricher_instance is None:
        _enricher_instance = GraphContextEnricher()
    return _enricher_instance.enrich(results)
