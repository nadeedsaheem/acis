# Implementation Plan — Production Repository Restructuring & Cleanup

Transform the repository from a research workspace into a clean, production-quality engineering repository suitable for senior engineer review.

## User Review Required

> [!IMPORTANT]
> This plan proposes moving, archiving, and deleting files across the entire repository. **No files will be deleted until you explicitly approve.** Every file is classified with a specific action and justification. Please review the full classification below before approving.

> [!WARNING]
> - The root `code_base.json` (43MB) and `data/code_base.json` (18MB) are duplicate datasets from different parser generations. The root version is the latest (2,711 files with call graph data). I propose keeping only the root version and symlinking or gitignoring the old one.
> - The `ACIS/` directory (proprietary source headers) is already in `.gitignore` — it will be left untouched.
> - The `project_analysis_report.pdf` is actually a markdown file with a `.pdf` extension. I'll rename it.

## Open Questions

> [!IMPORTANT]
> 1. **Should `data/code_base.json` (18MB, old dataset) be deleted or archived?** It's an older parser output with only 1,864 files vs the current 2,711 files.
> 2. **Should the `scratch/` directory (debug scripts) be archived entirely or deleted?** These are one-time Neo4j debug utilities.
> 3. **Do you want a `requirements.txt` or `pyproject.toml` generated?** Currently no dependency file exists.

---

## File Classification Report

### Root Directory Files

| File | Size | Action | Justification |
|:---|:---|:---|:---|
| `README.md` | 1.4KB | **REWRITE** | Outdated — references old structure, contains corrupted null bytes at end |
| `PROJECT_SUMMARY.md` | 1.3KB | **ARCHIVE** | Outdated — describes parser-only deliverable, not the full GraphRAG system |
| `.env.example` | 133B | **KEEP** | Configuration template — belongs at root |
| `.gitignore` | 43B | **UPDATE** | Must add: `logs/`, `*.log`, `graph_build.log`, `parse_summary.json`, `failed_files.json`, `__pycache__/` |
| `start_server.ps1` | 579B | **MOVE** → `scripts/` | Utility launch script |
| `code_base.json` | 43MB | **MOVE** → `data/` | Production dataset — should not be at root |
| `parse_summary.json` | 308B | **DELETE** | Generated build artifact |
| `failed_files.json` | 2B | **DELETE** | Empty generated artifact (`[]`) |
| `graph_build.log` | 11KB | **DELETE** | Runtime log — add to `.gitignore` |
| `spa_position_trace.py` | 2.3KB | **ARCHIVE** | One-time debug trace script |
| `spa_position_trace.md` | 7.6KB | **ARCHIVE** | One-time debug trace report |
| `project_analysis_report.pdf` | 7.9KB | **ARCHIVE** | Misnamed `.pdf` (is actually markdown) |
| `project_analysis_report.md` | 7.9KB | **ARCHIVE** | Duplicate of .pdf file — old project analysis |

### Root-Level Reports (26 files → MOVE to `docs/reports/`)

All phase certification and validation reports at root should be consolidated:

| Files | Action | Justification |
|:---|:---|:---|
| `phase6_certification.md`, `phase6_validation_report.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase7b_certification.md`, `phase7b_validation_report.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_certification.md`, `phase9_validation_report.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_1_certification.md`, `phase9_1_validation_report.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_3_certification.md`, `phase9_3_1_certification.md`, `phase9_3_1_validation.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_4_certification.md`, `phase9_4_validation.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_5_certification.md`, `phase9_5_validation.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_6_certification.md`, `phase9_6_validation.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase9_7_certification.md`, `phase9_7_validation.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase10_certification.md`, `phase10_validation.md`, `phase10_1_certification.md`, `phase10_1_validation.md`, `phase10_2_certification.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase11_certification.md`, `phase11_validation.md` | **MOVE** → `docs/reports/` | Historical phase reports |
| `phase13_certification.md` | **MOVE** → `docs/reports/` | Latest phase report |
| `call_graph_report.md` | **MOVE** → `docs/reports/` | Phase 13 report |
| `workflow_retrieval_report.md` | **MOVE** → `docs/reports/` | Phase 13 report |
| `compile_commands_report.md` | **MOVE** → `docs/reports/` | Phase 12 report |
| `fqn_collision_report.md` | **MOVE** → `docs/reports/` | Phase 11 report |
| `fqn_migration_report.md` | **MOVE** → `docs/reports/` | Phase 11 report |

### Root-Level Analysis Documents (MOVE to `docs/`)

| File | Action | Justification |
|:---|:---|:---|
| `acis_graphrag_system_report.md` | **MOVE** → `docs/` | System architecture document |
| `architecture_risk_report.md` | **MOVE** → `docs/` | Audit report |
| `production_gap_analysis.md` | **MOVE** → `docs/` | Audit report |
| `missing_components.md` | **MOVE** → `docs/` | Audit report |
| `scaling_analysis.md` | **MOVE** → `docs/` | Audit report |
| `recommended_roadmap.md` | **MOVE** → `docs/` | Roadmap document |

### Root-Level Legacy Reports (ARCHIVE)

| File | Action | Justification |
|:---|:---|:---|
| `answer_quality_report.md` | **ARCHIVE** | Old quality audit — superseded by later phases |
| `cleanup_certification.md` | **ARCHIVE** | Old cleanup — superseded by this restructuring |
| `cleanup_plan.md` | **ARCHIVE** | Old cleanup plan |
| `cleanup_report.md` | **ARCHIVE** | Old cleanup report |
| `context_enrichment_report.md` | **ARCHIVE** | Phase 9 era report |
| `duplicate_file_report.md` | **ARCHIVE** | Old audit report |
| `graph_relationship_rendering_report.md` | **ARCHIVE** | Phase 9 era report |
| `grounding_quality_report.md` | **ARCHIVE** | Phase 9 era report |
| `neo4j_query_modernization.md` | **ARCHIVE** | One-time refactor notes |
| `primary_entity_resolution_report.md` | **ARCHIVE** | Phase 10 era report |
| `regression_analysis_report.md` | **ARCHIVE** | One-time regression analysis |
| `repository_structure_after_cleanup.md` | **ARCHIVE** | Old cleanup output |
| `response_format_report.md` | **ARCHIVE** | Phase 9 era report |
| `response_rendering_report.md` | **ARCHIVE** | Phase 9 era report |

---

### `src/` Directory — Production Code Classification

#### KEEP (Core Production Pipeline — 21 files)

| File | Layer | Role |
|:---|:---|:---|
| `multi_repo.py` | Parser | C++ AST parser with tree-sitter |
| `namespace_tracker.py` | Parser | Namespace scope tracking |
| `fqn_resolver.py` | Parser | Fully qualified name resolution |
| `call_extractor.py` | Parser | Function call extraction from AST |
| `compilation_database.py` | Parser | compile_commands.json loader |
| `include_resolver.py` | Parser | #include path resolution |
| `macro_registry.py` | Parser | Preprocessor macro tracking |
| `conditional_evaluator.py` | Parser | #ifdef branch evaluation |
| `build_graph.py` | Graph | Neo4j graph builder & schema |
| `call_graph_builder.py` | Graph | CALLS/CALLED_BY relationship loader |
| `graph_context_enricher.py` | Graph | Neo4j context enrichment + call trees |
| `graph_relationship_renderer.py` | Graph | Structured relationship display |
| `graph_evidence_renderer.py` | Graph | Knowledge graph evidence display |
| `embed_docs.py` | Retrieval | Embedding generation & semantic search |
| `retriever.py` | Retrieval | Hybrid retrieval (vector + lexical) |
| `intent_entity_ranker.py` | Retrieval | Intent detection & result ranking |
| `primary_entity_resolver.py` | Retrieval | Primary entity resolution |
| `entity_scoring.py` | Retrieval | Entity scoring heuristics |
| `context_builder.py` | LLM | Context assembly for LLM |
| `grounded_answer_synthesizer.py` | LLM | Prompt engineering (canonical) |
| `response_composer.py` | LLM | Final response composition |
| `llm_provider.py` | LLM | Gemini API integration |
| `query_normalizer.py` | LLM | Query normalization |
| `api_server.py` | API | FastAPI REST server |
| `api_models.py` | API | Pydantic request/response models |
| `graphrag_service.py` | API | Service orchestrator |

#### ARCHIVE (Superseded Implementations — 4 files)

| File | Superseded By | Justification |
|:---|:---|:---|
| `answer_synthesizer.py` | `grounded_answer_synthesizer.py` | Old prompt builder — not imported anywhere |
| `response_formatter.py` | `response_composer.py` | Old formatter — not imported anywhere |
| `response_renderer.py` | `response_composer.py` + `graph_relationship_renderer.py` | Old renderer — not imported anywhere |
| `relationship_presenter.py` | `graph_relationship_renderer.py` | Old presenter — not imported anywhere |

#### MOVE to `tools/` (Standalone Utilities — 3 files)

| File | Justification |
|:---|:---|
| `rebuild_embeddings.py` | One-time migration utility — standalone CLI |
| `generate_fqn_reports.py` | One-time FQN report generator — standalone CLI |
| `chat.py` | Interactive CLI demo — not part of production pipeline |

#### MOVE to `tests/` (Phase Validation Scripts — 10 files)

| File | Justification |
|:---|:---|
| `phase9_3_validation.py` | Phase 9.3 test suite |
| `phase9_3_1_validation.py` | Phase 9.3.1 test suite |
| `phase9_4_validation.py` | Phase 9.4 test suite |
| `phase9_5_validation.py` | Phase 9.5 test suite |
| `phase9_6_validation.py` | Phase 9.6 test suite |
| `phase9_7_validation.py` | Phase 9.7 test suite |
| `phase10_validation.py` | Phase 10 test suite |
| `phase10_1_validation.py` | Phase 10.1 test suite |
| `phase10_2_validation.py` | Phase 10.2 test suite |
| `phase11_validation.py` | Phase 11 test suite |
| `phase12_validation.py` | Phase 12 test suite |
| `phase13_validation.py` | Phase 13 test suite |

---

### `tests/` Directory

| File | Action | Justification |
|:---|:---|:---|
| `communication_layer_validation.py` | **KEEP** | Integration test for API |
| `integration_test.py` | **KEEP** | Core integration test |
| `mock_repo/` | **KEEP** | Test fixtures for Phase 12 |
| `phase7b2_validation.py` | **KEEP** | Phase 7b2 test |
| `phase9_2_validation.py` | **KEEP** | Phase 9.2 test |
| `real_llm_validation.py` | **KEEP** | LLM integration test |
| `test_fallback_handling.py` | **KEEP** | Fallback test |
| `test_gemini.py` | **ARCHIVE** | Simple Gemini smoke test — 496 bytes |
| `verify_retriever.py` | **KEEP** | Retriever verification |

---

### `reports/` Directory (56 files)

| Action | Justification |
|:---|:---|
| **MOVE entire directory** → `docs/reports/` | Consolidate all reports under `docs/` |

---

### `archive/` Directory

| Action | Justification |
|:---|:---|
| **KEEP as-is** | Already contains archived experimental code — will receive additional archived files |

---

### `scratch/` Directory (5 files)

| File | Action | Justification |
|:---|:---|:---|
| `check_neo4j.py` | **ARCHIVE** | One-time DB inspection script |
| `rebuild_graph.py` | **ARCHIVE** | One-time graph rebuild script (superseded by `build_graph.py` CLI) |
| `test_bytes.py` | **DELETE** | Trivial 382-byte debug script |
| `test_queries.py` | **ARCHIVE** | One-time query test |
| `verify_db.py` | **ARCHIVE** | One-time DB verification |

---

### `data/` Directory

| File | Action | Justification |
|:---|:---|:---|
| `code_base.json` (18MB) | **ARCHIVE** | Old parser output (1,864 files). Root `code_base.json` (2,711 files) is canonical |
| `class_names.txt` | **ARCHIVE** | One-time extraction artifact |

---

### `logs/` Directory

| Action | Justification |
|:---|:---|
| **DELETE contents, keep directory, add to `.gitignore`** | Runtime logs should never be committed |

---

## Target Repository Structure

```
project_root/
│
├── README.md                          # Rewritten — professional overview
├── .env.example                       # Configuration template
├── .gitignore                         # Updated with comprehensive exclusions
│
├── src/                               # All production source code
│   ├── parser/                        # C++ AST parsing layer
│   │   ├── __init__.py
│   │   ├── multi_repo.py
│   │   ├── namespace_tracker.py
│   │   ├── fqn_resolver.py
│   │   ├── call_extractor.py
│   │   ├── compilation_database.py
│   │   ├── include_resolver.py
│   │   ├── macro_registry.py
│   │   └── conditional_evaluator.py
│   │
│   ├── graph/                         # Neo4j knowledge graph layer
│   │   ├── __init__.py
│   │   ├── build_graph.py
│   │   ├── call_graph_builder.py
│   │   ├── graph_context_enricher.py
│   │   ├── graph_relationship_renderer.py
│   │   └── graph_evidence_renderer.py
│   │
│   ├── retrieval/                     # Search & entity resolution layer
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   ├── embed_docs.py
│   │   ├── intent_entity_ranker.py
│   │   ├── primary_entity_resolver.py
│   │   ├── entity_scoring.py
│   │   └── query_normalizer.py
│   │
│   ├── llm/                           # LLM integration layer
│   │   ├── __init__.py
│   │   ├── llm_provider.py
│   │   ├── context_builder.py
│   │   ├── grounded_answer_synthesizer.py
│   │   └── response_composer.py
│   │
│   └── api/                           # FastAPI service layer
│       ├── __init__.py
│       ├── api_server.py
│       ├── api_models.py
│       └── graphrag_service.py
│
├── tests/                             # All test & validation suites
│   ├── mock_repo/                     # Test fixtures
│   ├── integration_test.py
│   ├── communication_layer_validation.py
│   ├── test_fallback_handling.py
│   ├── verify_retriever.py
│   ├── real_llm_validation.py
│   ├── phase7b2_validation.py
│   ├── phase9_2_validation.py
│   ├── phase9_3_validation.py         # Moved from src/
│   ├── phase9_3_1_validation.py       # Moved from src/
│   ├── phase9_4_validation.py         # Moved from src/
│   ├── phase9_5_validation.py         # Moved from src/
│   ├── phase9_6_validation.py         # Moved from src/
│   ├── phase9_7_validation.py         # Moved from src/
│   ├── phase10_validation.py          # Moved from src/
│   ├── phase10_1_validation.py        # Moved from src/
│   ├── phase10_2_validation.py        # Moved from src/
│   ├── phase11_validation.py          # Moved from src/
│   ├── phase12_validation.py          # Moved from src/
│   └── phase13_validation.py          # Moved from src/
│
├── tools/                             # Standalone utility scripts
│   ├── rebuild_embeddings.py          # One-time embedding rebuilder
│   ├── generate_fqn_reports.py        # FQN collision/migration report generator
│   └── chat.py                        # Interactive CLI demo
│
├── scripts/                           # Launcher scripts
│   └── start_server.ps1               # Server startup script
│
├── data/                              # Production datasets
│   └── code_base.json                 # Canonical parser output (moved from root)
│
├── docs/                              # All documentation & reports
│   ├── acis_graphrag_system_report.md
│   ├── architecture_risk_report.md
│   ├── production_gap_analysis.md
│   ├── missing_components.md
│   ├── scaling_analysis.md
│   ├── recommended_roadmap.md
│   └── reports/                       # Phase validation reports (consolidated)
│       ├── (all 56 files from reports/)
│       └── (all root-level phase*.md files)
│
├── logs/                              # Runtime logs (gitignored)
│
└── archive/                           # Archived experiments & superseded code
    ├── superseded_src/                # Old implementations
    │   ├── answer_synthesizer.py
    │   ├── response_formatter.py
    │   ├── response_renderer.py
    │   └── relationship_presenter.py
    ├── debug/                         # (existing)
    ├── dev_tools/                     # (existing)
    ├── experiments/                   # (existing)
    ├── tests/                         # (existing)
    └── legacy_reports/                # Old root reports
```

---

## Import Cleanup

All current `src/` imports use flat module names (e.g., `from retriever import semantic_search`). Moving files into subpackages (`src/parser/`, `src/graph/`, etc.) would **break every import** in the codebase.

**Proposed approach — Flat with `__init__.py` re-exports:**
- Keep all production `.py` files in `src/` (flat) for now to preserve all imports.
- Create `src/parser/`, `src/graph/`, `src/retrieval/`, `src/llm/`, `src/api/` as **logical grouping directories** with `__init__.py` files that re-export from the flat modules.
- This maintains backward compatibility while providing clear architectural documentation.

**Alternative approach — Full subpackage migration:**
- Move files into subpackages and update all internal imports.
- Higher risk, higher reward — makes the architecture physically match the logical layers.
- Requires updating 50+ import statements across all files.

> [!IMPORTANT]
> **Which approach do you prefer?** I recommend the **flat structure with documentation** for safety, since the flat layout is already clean with 26 production files and clear naming conventions. The subpackage approach is better for larger teams but carries refactoring risk.

---

## `.gitignore` Update

```gitignore
# Proprietary source
ACIS/

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/

# Environment
.env
gmni.env

# Runtime artifacts
logs/
*.log
graph_build.log
parse_summary.json
failed_files.json

# Large data (optional — uncomment if using Git LFS)
# data/code_base.json
```

---

## New `README.md` Outline

The README will be rewritten to include:
1. **Project Title & Badge** — ACIS GraphRAG Code Intelligence System
2. **Architecture Overview** — 5-layer diagram (Parser → Graph → Retrieval → LLM → API)
3. **Quick Start** — Environment setup, Neo4j configuration, server launch
4. **Directory Structure** — Annotated tree
5. **Entry Points** — `api_server.py`, `build_graph.py`, `multi_repo.py`
6. **Technology Stack** — tree-sitter, Neo4j, sentence-transformers, Gemini, FastAPI

---

## Execution Steps

1. Create target directories (`docs/`, `docs/reports/`, `tools/`, `scripts/`, `archive/superseded_src/`, `archive/legacy_reports/`)
2. Move root-level reports → `docs/reports/`
3. Move root-level analysis docs → `docs/`
4. Move root-level legacy reports → `archive/legacy_reports/`
5. Move `start_server.ps1` → `scripts/`
6. Move `code_base.json` → `data/` (overwrite old one)
7. Archive superseded `src/` files → `archive/superseded_src/`
8. Move validation scripts from `src/` → `tests/`
9. Move standalone tools from `src/` → `tools/`
10. Archive `scratch/` files → `archive/`
11. Archive `data/class_names.txt` and old `data/code_base.json`
12. Update `.gitignore`
13. Delete generated artifacts (`parse_summary.json`, `failed_files.json`, `graph_build.log`, `logs/` contents)
14. Rewrite `README.md`
15. Generate `docs/dependency_graph.md`
16. Generate `docs/repository_structure.md`

---

## Verification Plan

### Automated Tests
- After restructuring, run `python src/api_server.py` and verify server starts successfully.
- Run `python src/phase13_validation.py` (if kept in src) to verify imports still work.
- Verify all production imports resolve correctly by running a smoke test.

### Manual Verification
- Review the final `git status` output to confirm all moves are tracked.
- Inspect the repository structure matches the target layout.
