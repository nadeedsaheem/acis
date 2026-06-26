# Repository Structure After Cleanup

```text
ACIS-GraphRAG/
│
├── src/                        # Core Production Files
│   ├── api_server.py
│   ├── api_models.py
│   ├── graphrag_service.py
│   ├── retriever.py
│   ├── query_normalizer.py
│   ├── context_builder.py
│   ├── llm_provider.py
│   ├── embed_docs.py
│   ├── rebuild_embeddings.py
│   ├── build_graph.py
│   └── multi_repo.py
│
├── tests/                      # Validation & Testing
│   ├── integration_test.py
│   ├── real_llm_validation.py
│   ├── communication_layer_validation.py
│   ├── phase7b2_validation.py
│   ├── phase9_2_validation.py
│   ├── verify_retriever.py
│   └── test_gemini.py
│
├── data/                       # Ingestion Data
│   ├── code_base.json
│   └── class_names.txt
│
├── reports/                    # Generated Phase Reports & Certifications
│   ├── architecture_final_report.md
│   ├── phase2_report.md
│   ├── phase*_certification.md
│   ├── *_validation_report.md
│   └── ... (40+ reports)
│
├── logs/                       # System Logs
│   ├── api.log
│   └── graph_build.log
│
├── archive/                    
│   └── dev_tools/              # Deprecated/One-time scripts
│       ├── generate_reports.py
│       ├── analyze.py
│       ├── check_db.py
│       └── ...
│
├── README.md                   # Project Documentation
├── PROJECT_SUMMARY.md          # Executive Summary
├── .env.example                # Environment Placeholders
├── .gitignore                  # Git Configuration
├── cleanup_plan.md             # This document
├── duplicate_file_report.md    # Recommendations for deleting duplicates
├── repository_structure_after_cleanup.md # This document
└── cleanup_certification.md    # Final Certification
```

## Root Folder Cleanliness
The root folder has been successfully reduced from ~100 files to ~14 items, strictly organizing code, logs, tests, data, and legacy scripts into clean, self-contained directories.
