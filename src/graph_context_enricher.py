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

    def enrich(self, results, query=None):
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
        CALL (n) {
            OPTIONAL MATCH (n)-[:CALLS]->(called)
            RETURN collect(called.name) AS calls
        }
        CALL (n) {
            OPTIONAL MATCH (caller)-[:CALLS]->(n)
            RETURN collect(caller.name) AS called_by
        }
        
        RETURN e.name AS name, e.entity_type AS entity_type,
               child_classes, parent_classes, methods, returned_by, 
               used_as_parameter, returns_types, owning_classes, enum_values,
               calls, called_by
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
                        "enum_values": clean(r.get("enum_values", [])),
                        "calls": clean(r.get("calls", [])),
                        "called_by": clean(r.get("called_by", []))
                    }
        except Exception as e:
            print(f"Error enriching context: {e}")
            
        # Merge back into results
        enriched_results = []
        
        # Check if this is a workflow query
        is_wf = False
        if query:
            lower_q = query.lower()
            workflow_keywords = ["how does", "how is", "what happens when", "call graph", "trace", "calls", "workflow", "implementation of"]
            is_wf = any(kw in lower_q for kw in workflow_keywords) or ("work" in lower_q and "how" in lower_q) or ("happen" in lower_q and "call" in lower_q)

        for r in results:
            name = r.get("name") or r.get("entity_name") or ""
            key = f"{r.get('entity_type')}::{name}"
            rels = enrichment_map.get(key, {})
            
            # Map into the expected structure
            new_r = {
                "entity": {
                    "type": r.get("entity_type", "Entity"),
                    "name": name,
                    "fqn": r.get("fqn", "")
                },
                "fqn": r.get("fqn", ""),
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
            if rels.get("calls"): new_r["relationships"]["calls"] = rels["calls"]
            if rels.get("called_by"): new_r["relationships"]["called_by"] = rels["called_by"]
            
            # Include old params if present
            if r.get("parameters"):
                new_r["relationships"]["parameters"] = [p.get('name') for p in r['parameters'] if isinstance(p, dict)]
                
            # If it's a workflow query and this is a Function/Method, fetch the depth-2 call graph
            if is_wf and r.get("entity_type") in ["Function", "Method"]:
                start_fqn = r.get("fqn") or name
                start_id = r.get("entity_id", "")
                calls_depth2 = self.get_call_graph_depth2(start_id, start_fqn)
                if calls_depth2:
                    new_r["call_graph"] = calls_depth2
                    new_r["call_graph_tree"] = self.format_call_graph_tree(calls_depth2, start_fqn)
                
            enriched_results.append(new_r)
            
        return enriched_results

    def get_call_graph_depth2(self, entity_id, entity_fqn):
        cypher = """
        MATCH (start) WHERE (start:Function OR start:Method) AND (start.id = $id OR start.fqn = $fqn)
        OPTIONAL MATCH path = (start)-[:CALLS*1..2]->(callee)
        WITH path WHERE path IS NOT NULL
        UNWIND relationships(path) AS r
        RETURN DISTINCT startNode(r).fqn AS caller_fqn, startNode(r).name AS caller_name, labels(startNode(r))[0] AS caller_type,
                        endNode(r).fqn AS callee_fqn, endNode(r).name AS callee_name, labels(endNode(r))[0] AS callee_type,
                        r.line AS line
        """
        calls = []
        try:
            with self.driver.session() as session:
                records = session.run(cypher, id=entity_id, fqn=entity_fqn)
                for r in records:
                    calls.append({
                        "caller_fqn": r["caller_fqn"],
                        "caller_name": r["caller_name"],
                        "caller_type": r["caller_type"],
                        "callee_fqn": r["callee_fqn"],
                        "callee_name": r["callee_name"],
                        "callee_type": r["callee_type"],
                        "line": r["line"]
                    })
        except Exception as e:
            print(f"Error fetching call graph: {e}")
        return calls

    def format_call_graph_tree(self, calls, start_fqn):
        if not calls:
            return ""
        adj = {}
        fqn_to_name = {}
        for c in calls:
            caller = c["caller_fqn"]
            callee = c["callee_fqn"]
            fqn_to_name[caller] = c["caller_name"]
            fqn_to_name[callee] = c["callee_name"]
            if caller not in adj:
                adj[caller] = []
            adj[caller].append((callee, c["line"]))
            
        lines = []
        seen = set()
        
        def dfs(fqn, depth=0):
            name = fqn_to_name.get(fqn, fqn.split("::")[-1])
            indent = "  " * depth
            lines.append(f"{indent}- {name}()")
            if fqn in seen:
                return
            seen.add(fqn)
            
            callees = adj.get(fqn, [])
            callees_sorted = sorted(callees, key=lambda x: x[1])
            for callee, line in callees_sorted:
                dfs(callee, depth + 1)
                
        dfs(start_fqn, 0)
        return "\n".join(lines)

# Expose a singleton-like enricher
_enricher_instance = None

def enrich_context(results: list, query: str = None) -> list:
    global _enricher_instance
    if _enricher_instance is None:
        _enricher_instance = GraphContextEnricher()
    return _enricher_instance.enrich(results, query)
