import json
import os
import re

def run_audit():
    clean_file = "all_entities_clean.json"
    if not os.path.exists(clean_file):
        print(f"Error: Cleaned file '{clean_file}' not found.")
        return

    with open(clean_file, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"Loaded {len(dataset)} files from '{clean_file}'.")

    # 1. Schema Validation
    expected_fields = {
        "file", "path", "classes", "structs", "enums", "typedefs", 
        "namespaces", "includes", "methods", "functions", "inheritance"
    }
    
    missing_fields_count = 0
    type_mismatch_count = 0
    null_values_count = 0
    empty_strings_count = 0
    
    for item in dataset:
        # Check field presence
        for field in expected_fields:
            if field not in item:
                missing_fields_count += 1
                
        # Check types
        if not isinstance(item.get("file", ""), str): type_mismatch_count += 1
        if not isinstance(item.get("path", ""), str): type_mismatch_count += 1
        if not isinstance(item.get("classes", []), list): type_mismatch_count += 1
        if not isinstance(item.get("structs", []), list): type_mismatch_count += 1
        if not isinstance(item.get("enums", []), list): type_mismatch_count += 1
        if not isinstance(item.get("typedefs", []), list): type_mismatch_count += 1
        if not isinstance(item.get("namespaces", []), list): type_mismatch_count += 1
        if not isinstance(item.get("includes", []), list): type_mismatch_count += 1
        if not isinstance(item.get("methods", []), list): type_mismatch_count += 1
        if not isinstance(item.get("functions", []), list): type_mismatch_count += 1
        if not isinstance(item.get("inheritance", []), list): type_mismatch_count += 1
        
        # Check for null values and empty strings in key identifiers
        if item.get("file") is None or item.get("path") is None:
            null_values_count += 1
        if item.get("file") == "" or item.get("path") == "":
            empty_strings_count += 1

    print("\n--- SCHEMA VALIDATION RESULTS ---")
    print(f"Missing fields count: {missing_fields_count}")
    print(f"Type mismatch count: {type_mismatch_count}")
    print(f"Null values in path/file: {null_values_count}")
    print(f"Empty strings in path/file: {empty_strings_count}")

    # Collect global registries
    all_local_classes = set()
    all_local_structs = set()
    all_local_types = set() # classes + structs
    
    for item in dataset:
        for cls in item.get("classes", []):
            all_local_classes.add(cls.get("name", ""))
            all_local_types.add(cls.get("name", ""))
        for st in item.get("structs", []):
            all_local_structs.add(st.get("name", ""))
            all_local_types.add(st.get("name", ""))

    # 2. Data Quality Audit
    duplicate_files = len(dataset) - len({item.get("path") for item in dataset})
    
    total_inheritance = 0
    duplicate_inheritance = 0
    seen_inheritance = set()
    
    malformed_signatures = 0
    empty_names = 0
    
    methods_count = 0
    functions_count = 0
    
    for item in dataset:
        # Check inheritance duplicates
        for inh in item.get("inheritance", []):
            total_inheritance += 1
            pair = (inh.get("class"), inh.get("base"))
            if pair in seen_inheritance:
                duplicate_inheritance += 1
            seen_inheritance.add(pair)

        # Check methods
        for m in item.get("methods", []):
            methods_count += 1
            name = m.get("name", "")
            if not name:
                empty_names += 1
            if " " in name or "(" in name:
                if not (name.startswith("operator") or "operator" in name):
                    malformed_signatures += 1

        # Check functions
        for fn in item.get("functions", []):
            functions_count += 1
            name = fn.get("name", "")
            if not name:
                empty_names += 1
            if " " in name or "(" in name:
                if not (name.startswith("operator") or "operator" in name):
                    malformed_signatures += 1

    print("\n--- DATA QUALITY RESULTS ---")
    print(f"Duplicate file paths: {duplicate_files}")
    print(f"Total inheritance edges: {total_inheritance}")
    print(f"Duplicate inheritance edges: {duplicate_inheritance}")
    print(f"Total methods: {methods_count}")
    print(f"Total functions: {functions_count}")
    print(f"Empty function/method names: {empty_names}")
    print(f"Malformed names (braces/spaces outside operator): {malformed_signatures}")

    # 3. Relationship Validation
    # A: Methods referencing existing classes
    methods_with_missing_class = 0
    methods_with_class_found = 0
    methods_without_class_owner = 0
    
    for item in dataset:
        for m in item.get("methods", []):
            cls_name = m.get("class")
            if not cls_name:
                methods_without_class_owner += 1
                continue
            
            clean_cls = cls_name.split("::")[-1].strip()
            if clean_cls in all_local_types:
                methods_with_class_found += 1
            else:
                methods_with_missing_class += 1

    # B: Inheritance Classes Existence & Base Classification
    # Known external base class patterns
    known_external_bases = {
        "acis_ha_part_entity_mgr", "acis_ha_part_entity_mgr_factory", "acis_ha_part_entity_mgr_notifying",
        "CATBaseUnknown", "CATTopObject", "CATGeomHashTableBase", "CATCGMHashTableBase",
        "CATCGMVirtual", "CATCGMJournal", "CATTopology", "CATSurface", "CATCurve", "CATGeometry",
        "CATICGMUnknown", "CATMathStream", "CATMathStreamImpl", "ExportedByJS0DSPA", "ExportedByJS0CTYP",
        "ExportedByJS0ERROR", "ExportedByCATGMGeometricInterfaces", "ExportedByJS0INF",
        "ExportedByCATGMModelInterfaces", "ExportedByCATMathematics", "ExportedByYP00IMPL",
        "ExportedByCGMComponent", "ExportedByJS0CORBA", "IDispatch", "IUnknown", "CObject",
        "streambuf", "ios", "Operator", "__releaser__CGM", "CGMReleasable_uptr",
        "direct_render_mesh_manager", "rubberband_circle", "hoops_acis_entity_converter",
        "acis_hps_part_entity_mgr", "acis_hps_part_entity_mgr_factory", "hps_acis_entity_converter",
        "EventHandler", "WarningHandler", "ErrorHandler", "rubberband_driver", "rubberband_manager",
        "scheme_entity_converter"
    }

    local_bases_count = 0
    external_bases_count = 0
    unknown_bases_count = 0
    
    unresolved_bases = set()

    for item in dataset:
        for inh in item.get("inheritance", []):
            base = inh.get("base")
            if not base:
                continue
            
            clean_base = base.split("::")[-1].strip()
            
            # Check local definition
            if clean_base in all_local_types:
                local_bases_count += 1
            # Check external SDKs
            elif clean_base in known_external_bases or clean_base.startswith("CAT") or clean_base.startswith("ExportedBy"):
                external_bases_count += 1
            # Otherwise classified as UNKNOWN
            else:
                unknown_bases_count += 1
                unresolved_bases.add(clean_base)

    print("\n--- RELATIONSHIP VALIDATION ---")
    print(f"Methods with class owner matching local type: {methods_with_class_found}")
    print(f"Methods with class owner NOT matching local type: {methods_with_missing_class}")
    print(f"Methods without class owner listed: {methods_without_class_owner}")
    print(f"Inheritance bases: LOCAL: {local_bases_count} | EXTERNAL: {external_bases_count} | UNKNOWN: {unknown_bases_count}")
    print(f"Number of unique UNKNOWN bases: {len(unresolved_bases)}")
    if unresolved_bases:
        print("Sample UNKNOWN bases:", list(unresolved_bases)[:15])

if __name__ == "__main__":
    run_audit()
