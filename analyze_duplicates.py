import json
from collections import defaultdict

def analyze():
    with open('code_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Class name to list of file paths
    class_map = defaultdict(list)
    total_json_classes = 0
    total_json_inherits = 0
    
    # To trace missing inheritance edges, we need to know what inheritance edges exist
    # and whether they fail to be created due to the MERGE logic.
    # In Neo4j, MERGE (c1:Class {name: row.class_name}) MERGE (c2:Class {name: row.base_name})
    # MERGE (c1)-[:INHERITS]->(c2)
    # If c1 and c2 are merged by name, then an inheritance edge between "DuplicateClass" and "BaseClass" 
    # will only be created ONCE, even if it appears in multiple files.
    
    inheritance_edges = set() # Store unique (child, base) pairs

    for file_obj in data:
        path = file_obj.get('path', 'unknown')
        for cls in file_obj.get('classes', []):
            name = cls.get('name')
            if name:
                class_map[name].append(path)
                total_json_classes += 1
                
        for inh in file_obj.get('inheritance', []):
            c_name = inh.get('class')
            b_name = inh.get('base')
            if c_name and b_name:
                total_json_inherits += 1
                inheritance_edges.add((c_name, b_name))

    # Find duplicates
    duplicates = {name: paths for name, paths in class_map.items() if len(paths) > 1}
    
    # Calculate missing classes
    unique_class_names = len(class_map)
    duplicate_class_instances_lost = total_json_classes - unique_class_names
    
    unique_inheritance_edges = len(inheritance_edges)
    duplicate_inheritance_edges_lost = total_json_inherits - unique_inheritance_edges

    # Generate Markdown Report
    md = "# Duplicate Class Report\n\n"
    md += f"**Total Classes in JSON:** {total_json_classes}\n"
    md += f"**Unique Class Names:** {unique_class_names}\n"
    md += f"**Class Instances Lost due to Name Collision:** {duplicate_class_instances_lost}\n\n"
    
    md += f"**Total INHERITS in JSON:** {total_json_inherits}\n"
    md += f"**Unique INHERITS pairs:** {unique_inheritance_edges}\n"
    md += f"**INHERITS Edges Lost due to Name Collision:** {duplicate_inheritance_edges_lost}\n\n"
    
    md += "## Duplicate Classes Details\n\n"
    for name, paths in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
        md += f"### {name}\n"
        md += f"- **Occurrences:** {len(paths)}\n"
        md += "- **Files:**\n"
        for p in sorted(paths):
            md += f"  - `{p}`\n"
        md += "\n"
        
    with open('duplicate_class_report.md', 'w', encoding='utf-8') as f:
        f.write(md)
        
    print(f"Total JSON Classes: {total_json_classes}")
    print(f"Unique Class Names: {unique_class_names}")
    print(f"Missing Class Nodes (JSON - Unique): {duplicate_class_instances_lost}")
    print(f"Total JSON Inherits: {total_json_inherits}")
    print(f"Unique Inherits Pairs: {unique_inheritance_edges}")
    print(f"Missing Inherits Edges (JSON - Unique Pairs): {duplicate_inheritance_edges_lost}")

if __name__ == '__main__':
    analyze()
