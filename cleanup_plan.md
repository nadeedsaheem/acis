# Repository Cleanup Plan

## KEEP (Production & Core Files)
*Will be moved to appropriate folders (`src/`, `root`, `tests/`, `reports/`, `data/`, `logs/`)*

### Root & `src/` (Production)
- `api_server.py` -> `src/`
- `api_models.py` -> `src/`
- `graphrag_service.py` -> `src/`
- `retriever.py` -> `src/`
- `query_normalizer.py` -> `src/`
- `context_builder.py` -> `src/`
- `llm_provider.py` -> `src/`
- `embed_docs.py` -> `src/`
- `rebuild_embeddings.py` -> `src/`
- `build_graph.py` -> `src/`
- `multi_repo.py` -> `src/`
- `README.md` -> `root`
- `PROJECT_SUMMARY.md` -> `root`
- `.gitignore` -> `root`
- `requirements.txt` -> `root` (To be verified/created)
- `.env.example` -> `root` (To be created)

### `data/`
- `code_base.json`
- `class_names.txt`

### `tests/`
- `integration_test.py`
- `real_llm_validation.py`
- `communication_layer_validation.py`
- `phase7b2_validation.py`
- `phase9_2_validation.py`
- `verify_retriever.py`
- `test_gemini.py`

### `reports/`
- `api_contract_v2.md`
- `architecture_final_report.md`
- `cleanup_report.md`
- `delivery_checklist.md`
- `duplicate_class_report.md`
- `embedding_upgrade_report.md`
- `graph_build_report.md`
- `integration_contract.md`
- `method_collision_report.md`
- `method_resolution_report.md`
- `parameter_property_audit.md`
- `phase2_report.md`
- `phase2b_certification.md`
- `phase2b_failure_analysis.md`
- `phase2b_validation_report.md`
- `phase2c_certification.md`
- `phase2c_validation_report.md`
- `phase3_certification.md`
- `phase3_relationship_failure_report.md`
- `phase3_validation_report.md`
- `phase4_certification.md`
- `phase4_validation_report.md`
- `phase5_certification.md`
- `phase5_validation_report.md`
- `phase6_certification.md`
- `phase6_validation_report.md`
- `phase7b2_certification.md`
- `phase7b_certification.md`
- `phase7b_hardening_report.md`
- `phase7b_validation_report.md`
- `phase8_certification.md`
- `phase8_validation_report.md`
- `phase9_1_certification.md`
- `phase9_1_validation_report.md`
- `phase9_2_certification.md`
- `phase9_certification.md`
- `phase9_validation_report.md`
- `query_normalization_report.md`
- `real_llm_validation_report.md`
- `retrieval_certification.md`
- `retrieval_validation_report.md`
- `retriever_audit_report.md`
- `retriever_fix_validation_report.md`
- `return_type_statistics.md`
- `schema_refinement_report.md`
- `spaposition_audit_report.md`
- `subquery_refactor_report.md`
- `vector_api_migration_report.md`

### `logs/`
- `graph_build.log`
- `api.log` (Will remain in or be moved to `logs/`)

---

## ARCHIVE (Development & One-Time Scripts)
*Will be moved to `archive/dev_tools/`*
- `analyze.py`
- `analyze_duplicates.py`
- `analyze_methods.py`
- `analyze_phase2b.py`
- `audit_spaposition.py`
- `chat.py`
- `check_db.py`
- `check_db2.py`
- `check_returns.py`
- `check_spapos.py`
- `count_methods.py`
- `debug_norm.py`
- `extract_bad.py`
- `generate_phase2c.py`
- `generate_phase3.py`
- `generate_reports.py`
- `query_neo4j.py`
- `run_phase8_validation.py`
- `run_validation.py`
- `simulate_cypher.py`
- `test.py`
- `test_phase3.py`
- `test_syntax.py`
- `test_syntax2.py`

---

## DELETE
*Obvious temporary/debug files and environment variables that shouldn't be committed*
- `gmni.env` (Environment files should NEVER be committed; placeholder `.env.example` will replace it)
