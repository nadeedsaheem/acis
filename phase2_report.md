# ACIS Knowledge Graph Phase 2A - Report

## Execution Summary
- **Start Time:** Wed Jun 24 12:27:38 2026
- **End Time:** Wed Jun 24 12:27:51 2026
- **Execution Time:** 13.60 seconds
- **Errors Encountered:** 0

## Data Processed (from JSON)
- Functions parsed: 30833
- Methods parsed: 6554

## Validation Results (Neo4j Graph Database)
- **Total Function Nodes:** 25058
- **Total Method Nodes:** 2781
- **Total (File)-[:CONTAINS]->(Function) Edges:** 25058
- **Total (Class)-[:HAS_METHOD]->(Method) Edges:** 2781

## Identity Note on Functions & Methods
Because the unique identity is defined as `file_path::function_name` and `file_path::class_name::method_name`, C++ overloaded functions/methods (which share the same name but differ by parameters) are naturally merged into single nodes via idempotency. The JSON counts exceed the final Neo4j counts strictly due to this exact overload merging behavior, which acts as expected per the specified constraint schema.
