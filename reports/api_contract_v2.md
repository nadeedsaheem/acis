# GraphRAG System Integration Contract v2.0

This document defines the official API contract between the GraphRAG Backend (Central Server Team) and downstream consumers (Visual Studio Extension / Communication Layer Teams).

## Overview
- **Base URL:** `http://<host>:8000`
- **Protocol:** HTTP REST
- **Format:** `application/json`

---

## 1. Health Check

Used to verify backend availability, database connectivity, and LLM readiness.

**Endpoint:** `GET /health`

**Response Example (200 OK):**
```json
{
  "status": "healthy",
  "neo4j": "connected",
  "retriever": "ready",
  "llm": "ready",
  "repository": "ACIS",
  "version": "1.1"
}
```

---

## 2. Query Knowledge Graph

Primary endpoint for retrieving grounded RAG answers.

**Endpoint:** `POST /query`

### Request Schema

```json
{
  "repository": "ACIS",
  "query": "What is SPAposition?"
}
```
**Notes:**
- `repository` (string, required): Currently only `"ACIS"` is supported.
- `query` (string, required): The natural language query. Must not be empty.

### Response Schema (200 OK)

```json
{
  "query": "What is SPAposition?",
  "status": "success",
  "answer": "The graph context indicates that SPAposition...",
  "sources": [
    {
      "entity_type": "Class",
      "entity_name": "SPAposition",
      "repository": "ACIS",
      "score": 2.0
    }
  ],
  "retrieval_time": 0.045,
  "generation_time": 1.205,
  "total_time": 1.250
}
```

### Error Responses

The API uses graceful error handling without exposing internal stack traces.

**400 Bad Request (Invalid Repository):**
```json
{
  "status": "error",
  "success": false,
  "error": "Unsupported repository"
}
```

**400 Bad Request (Empty Query):**
```json
{
  "status": "error",
  "success": false,
  "error": "Query cannot be empty"
}
```

**503 Service Unavailable (Neo4j / Rate Limits):**
```json
{
  "status": "error",
  "success": false,
  "error": "Neo4j connection unavailable"
}
```

**504 Gateway Timeout (Request Timeout):**
```json
{
  "status": "error",
  "success": false,
  "error": "Request timeout"
}
```

---

## Timeout Protection
- `POST /query` requests are protected by a rigid **15-second timeout**. If the GraphRAG service fails to respond within this window, a `504 Gateway Timeout` will be returned.

## Security
- API keys (Neo4j, LLM) are fully abstracted by the backend and loaded securely via environment variables (`gmni.env` / system env). Downstream teams do NOT need API keys to call this service.
- Stack traces are completely sanitized and masked.
