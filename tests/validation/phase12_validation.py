import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

import os
import json
import shutil
import subprocess
import logging
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

MOCK_REPO_DIR = "tests/mock_repo"

def setup_mock_repo():
    logging.info("Setting up mock C++ repository...")
    if os.path.exists(MOCK_REPO_DIR):
        try:
            shutil.rmtree(MOCK_REPO_DIR)
        except Exception as e:
            logging.warning(f"Could not remove mock repository directory: {e}. Overwriting files in-place instead.")
        
    os.makedirs(f"{MOCK_REPO_DIR}/include", exist_ok=True)
    
    # 1. include/helper.h
    with open(f"{MOCK_REPO_DIR}/include/helper.h", "w", encoding="utf-8") as f:
        f.write("""#pragma once
class HelperClass {
    void help() {}
};
""")

    # 2. main.cpp
    with open(f"{MOCK_REPO_DIR}/main.cpp", "w", encoding="utf-8") as f:
        f.write("""#include "helper.h"

#ifdef DEBUG
class DebugLogger {
    void log(const char* msg) {}
};
#endif

#ifdef RELEASE
class OptimizedLogger {
    void log(const char* msg) {}
};
#endif

#ifdef _WIN32
class WindowsService {
    void runWin() {}
};
#else
class LinuxService {
    void runLinux() {}
};
#endif
""")

    # 3. compile_commands_debug.json
    db_debug = [
        {
            "directory": os.path.abspath(MOCK_REPO_DIR).replace("\\", "/"),
            "command": f"clang++ -Iinclude -DDEBUG=1 -D_WIN32 -std=c++20 main.cpp",
            "file": "main.cpp"
        }
    ]
    with open(f"{MOCK_REPO_DIR}/compile_commands_debug.json", "w", encoding="utf-8") as f:
        json.dump(db_debug, f, indent=2)
        
    # 4. compile_commands_release.json
    db_release = [
        {
            "directory": os.path.abspath(MOCK_REPO_DIR).replace("\\", "/"),
            "command": f"clang++ -Iinclude -DRELEASE=1 -std=c++20 main.cpp",
            "file": "main.cpp"
        }
    ]
    with open(f"{MOCK_REPO_DIR}/compile_commands_release.json", "w", encoding="utf-8") as f:
        json.dump(db_release, f, indent=2)
    logging.info("Mock repository setup complete.")

def run_parser_cli(compilation_db=None, config="Default", repo_root=MOCK_REPO_DIR):
    cmd = [
        "python", "src/parser/multi_repo.py",
        "--repo-root", repo_root,
        "--config", config
    ]
    if compilation_db:
        cmd.extend(["--compilation-db", compilation_db])
        
    logging.info(f"Running parser command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        logging.error(f"Parser failed:\nStdout: {result.stdout}\nStderr: {result.stderr}")
        raise RuntimeError("Parser run failed")
    
    # Load and return generated code_base.json
    with open("code_base.json", "r", encoding="utf-8") as f:
        return json.load(f)

def run_neo4j_loader():
    logging.info("Loading parsed data into Neo4j...")
    # Import build_graph class
    from graph.build_graph import KnowledgeGraphBuilder
    
    # Use user designated credentials
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "nadeed@3973"
    
    builder = KnowledgeGraphBuilder(uri, user, password)
    if not builder.driver:
        raise ConnectionError("Failed to connect to Neo4j database")
        
    # Reset database first
    builder.reset_database()
    builder.create_constraints()
    
    # Load data
    data = builder.load_data("code_base.json")
    stats = builder.build_graph(data)
    builder.close()
    
    logging.info(f"Database build complete: {stats}")
    return stats

def verify_neo4j_relationships(expected_config):
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "nadeed@3973"
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        # Verify BuildConfiguration node properties
        config_res = session.run(
            "MATCH (b:BuildConfiguration {name: $name}) RETURN b.compiler AS compiler, b.standard AS standard",
            name=expected_config
        ).single()
        
        if not config_res:
            driver.close()
            return False, f"BuildConfiguration node '{expected_config}' not found"
            
        compiler = config_res["compiler"]
        standard = config_res["standard"]
        
        # Verify File COMPILED_WITH relationship
        file_res = session.run(
            "MATCH (f:File {path: 'main.cpp'})-[:COMPILED_WITH]->(b:BuildConfiguration {name: $name}) RETURN count(f) AS count",
            name=expected_config
        ).single()["count"]
        
        if file_res != 1:
            driver.close()
            return False, f"File 'main.cpp' COMPILED_WITH BuildConfiguration relationship not found"
            
        # Verify File INCLUDES relationship
        includes_res = session.run(
            "MATCH (f1:File {path: 'main.cpp'})-[:INCLUDES]->(f2:File {path: 'include/helper.h'}) RETURN count(f1) AS count"
        ).single()["count"]
        
        if includes_res != 1:
            driver.close()
            return False, "File 'main.cpp' INCLUDES 'include/helper.h' relationship not found"

        # Verify entity ACTIVE_IN_CONFIGURATION relationship
        active_res = session.run(
            "MATCH (c:Class)-[r:ACTIVE_IN_CONFIGURATION]->(b:BuildConfiguration {name: $name}) RETURN count(c) AS count",
            name=expected_config
        ).single()["count"]
        
        if active_res == 0:
            driver.close()
            return False, f"No Class active in configuration '{expected_config}' relationships found"
            
    driver.close()
    return True, "All Neo4j assertions passed!"

def run_validation():
    setup_mock_repo()
    
    report = []
    report.append("# Phase 12 - Compilation Database Integration Validation Report\n")
    
    metrics = {
        "include_resolution_accuracy": 0.0,
        "macro_resolution_accuracy": 0.0,
        "conditional_branch_accuracy": 0.0,
        "backward_compatibility": "FAIL"
    }

    try:
        # ==========================================================
        # TEST 1: DEBUG CONFIGURATION
        # ==========================================================
        logging.info("=== Running Test 1: Debug Configuration ===")
        db_debug_path = f"{MOCK_REPO_DIR}/compile_commands_debug.json"
        data_debug = run_parser_cli(compilation_db=db_debug_path, config="Debug")
        
        # Verify main.cpp record
        main_record = next((r for r in data_debug if r["path"] == "main.cpp"), None)
        assert main_record is not None, "main.cpp record not parsed"
        
        # Includes checks
        resolved_includes = main_record.get("includes", [])
        logging.info(f"Debug Resolved includes: {resolved_includes}")
        assert "include/helper.h" in resolved_includes, "Failed to resolve helper.h"
        
        # Class checks
        classes = [c["name"] for c in main_record.get("classes", [])]
        logging.info(f"Debug classes: {classes}")
        assert "DebugLogger" in classes, "DebugLogger should be parsed"
        assert "OptimizedLogger" not in classes, "OptimizedLogger should NOT be parsed"
        assert "WindowsService" in classes, "WindowsService should be parsed"
        assert "LinuxService" not in classes, "LinuxService should NOT be parsed"
        
        # Load into Neo4j and check relationships
        run_neo4j_loader()
        neo4j_ok, neo4j_msg = verify_neo4j_relationships("Debug")
        logging.info(f"Neo4j verification for Debug: {neo4j_msg}")
        assert neo4j_ok, f"Neo4j assertions failed: {neo4j_msg}"
        
        # ==========================================================
        # TEST 2: RELEASE CONFIGURATION
        # ==========================================================
        logging.info("=== Running Test 2: Release Configuration ===")
        db_release_path = f"{MOCK_REPO_DIR}/compile_commands_release.json"
        data_release = run_parser_cli(compilation_db=db_release_path, config="Release")
        
        main_record_rel = next((r for r in data_release if r["path"] == "main.cpp"), None)
        assert main_record_rel is not None, "main.cpp record not parsed"
        
        # Includes checks
        resolved_includes_rel = main_record_rel.get("includes", [])
        logging.info(f"Release Resolved includes: {resolved_includes_rel}")
        assert "include/helper.h" in resolved_includes_rel, "Failed to resolve helper.h"
        
        # Class checks
        classes_rel = [c["name"] for c in main_record_rel.get("classes", [])]
        logging.info(f"Release classes: {classes_rel}")
        assert "DebugLogger" not in classes_rel, "DebugLogger should NOT be parsed"
        assert "OptimizedLogger" in classes_rel, "OptimizedLogger should be parsed"
        assert "WindowsService" not in classes_rel, "WindowsService should NOT be parsed"
        assert "LinuxService" in classes_rel, "LinuxService should be parsed"
        
        # Load into Neo4j and check relationships
        run_neo4j_loader()
        neo4j_ok_rel, neo4j_msg_rel = verify_neo4j_relationships("Release")
        logging.info(f"Neo4j verification for Release: {neo4j_msg_rel}")
        assert neo4j_ok_rel, f"Neo4j assertions failed: {neo4j_msg_rel}"
        
        # ==========================================================
        # TEST 3: BACKWARD COMPATIBILITY / FALLBACK
        # ==========================================================
        logging.info("=== Running Test 3: Legacy Fallback Mode ===")
        data_fallback = run_parser_cli(compilation_db=None, config="Default")
        
        main_record_fall = next((r for r in data_fallback if r["path"] == "main.cpp"), None)
        assert main_record_fall is not None, "main.cpp record not parsed"
        
        # In legacy mode (without compilation database), includes resolver uses fallback cache
        resolved_includes_fall = main_record_fall.get("includes", [])
        logging.info(f"Fallback Resolved includes: {resolved_includes_fall}")
        assert "include/helper.h" in resolved_includes_fall, "Fallback include resolution failed"
        
        # In legacy mode, macros aren't defined, so branches depending on DEBUG/RELEASE may be inactive,
        # but the parser successfully parses the file without crashing.
        logging.info("Legacy mode parsed successfully without error.")
        
        # Set metrics
        metrics["include_resolution_accuracy"] = 1.0
        metrics["macro_resolution_accuracy"] = 1.0
        metrics["conditional_branch_accuracy"] = 1.0
        metrics["backward_compatibility"] = "PASS"
        
        report.append("## Test Results Summary\n")
        report.append("| Test Case | Status | Detail |")
        report.append("|---|---|---|")
        report.append("| Debug Configuration Parsing | PASS | Correctly parsed DebugLogger and WindowsService |")
        report.append("| Release Configuration Parsing | PASS | Correctly parsed OptimizedLogger and LinuxService |")
        report.append("| Neo4j Graph Insertion & Schema | PASS | BuildConfiguration and relationships created |")
        report.append("| Legacy Fallback Mode | PASS | Runs successfully without compile commands |")
        
    except Exception as e:
        logging.error(f"Validation failed: {e}", exc_info=True)
        report.append(f"## Validation FAILED\nReason: {e}\n")
        
    # Write report
    with open("compile_commands_report.md", "w", encoding="utf-8") as f_rep:
        f_rep.write("\n".join(report))
        
    print(f"\nValidation metrics: {metrics}")
    return metrics

if __name__ == "__main__":
    run_validation()
