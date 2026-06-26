import os
import time
import logging
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from api_models import QueryRequest, QueryResponse, HealthResponse, ErrorResponse

SUPPORTED_REPOSITORIES = ["ACIS"]

# Setup Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ACIS GraphRAG API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logging.info("Warming up retriever model...")
    try:
        from retriever import semantic_search
        semantic_search("warmup")
        logging.info("Model warmed up successfully.")
    except Exception as e:
        logging.error(f"Failed to warm up model: {e}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    logging.error(f"Unhandled error: {error_msg}")
    
    if isinstance(exc, asyncio.TimeoutError):
        return JSONResponse(
            status_code=504,
            content={"status": "error", "success": False, "error": "Request timeout"}
        )
        
    return JSONResponse(
        status_code=500,
        content={"status": "error", "success": False, "error": "An internal error occurred during query execution"}
    )

@app.get("/health", response_model=HealthResponse)
def health_check():
    start_time = time.time()
    neo4j_status = "connected"
    retriever_status = "ready"
    llm_status = "ready"
    
    try:
        from neo4j import GraphDatabase
        URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        USER = os.getenv("NEO4J_USER", "neo4j")
        PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        driver.verify_connectivity()
        driver.close()
    except Exception as e:
        neo4j_status = "unavailable"
        logging.error(f"Health Check - Neo4j Error: {e}")
        
    execution_time = time.time() - start_time
    logging.info(f"Health check executed in {execution_time:.3f}s")
    
    return HealthResponse(
        status="healthy" if neo4j_status == "connected" else "degraded",
        neo4j=neo4j_status,
        retriever=retriever_status,
        llm=llm_status,
        repository="ACIS",
        version="1.1"
    )
def make_fallback_response(query: str, error_message: str, start_time: float) -> QueryResponse:
    from response_composer import compose_response
    fallback_data = {
        "query": query,
        "status": "error",
        "answer": error_message,
        "sources": [],
        "retrieval_time": 0.0,
        "generation_time": 0.0,
        "total_time": time.time() - start_time
    }
    fallback_data = compose_response(fallback_data)
    return QueryResponse(**fallback_data)

@app.post("/query", response_model=QueryResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}, 504: {"model": ErrorResponse}})
async def query_graphrag(request: QueryRequest):
    start_time = time.time()
    
    # 1. Validation
    if not request.query or not request.query.strip():
        logging.warning("Empty query received")
        return JSONResponse(status_code=400, content={"status": "error", "success": False, "error": "Query cannot be empty"})
        
    if request.repository not in SUPPORTED_REPOSITORIES:
        logging.warning(f"Unsupported repository requested: {request.repository}")
        return JSONResponse(status_code=400, content={"status": "error", "success": False, "error": "Unsupported repository"})
        
    # 2. Execution
    try:
        from query_normalizer import normalize_query
        request.query = normalize_query(request.query)
        logging.info(f"Executing query: {request.query}")
        from graphrag_service import answer_question
        
        # Try running the query with a retry on connection error
        max_retries = 2
        result = None
        for attempt in range(max_retries):
            try:
                # answer_question returns a dict with query, answer, sources, retrieval_time, generation_time, total_time
                # Wrap in asyncio timeout
                result = await asyncio.wait_for(
                    asyncio.to_thread(answer_question, request.query),
                    timeout=15.0
                )
                break
            except Exception as e:
                error_msg = str(e)
                is_connection_error = any(kw in error_msg.lower() for kw in ["connection", "bolt", "reset", "closed", "10054", "7687"])
                if is_connection_error and attempt < max_retries - 1:
                    logging.warning(f"Neo4j connection error (attempt {attempt + 1}/{max_retries}): {error_msg}. Resetting driver and retrying in 1s...")
                    await asyncio.sleep(1.0)
                    try:
                        # Reset the semantic retriever instance so it reconnects on next attempt
                        import retriever
                        if retriever._semantic_retriever_instance:
                            retriever._semantic_retriever_instance.close()
                            retriever._semantic_retriever_instance = None
                    except Exception as reset_err:
                        logging.error(f"Error resetting retriever instance: {reset_err}")
                    continue
                raise e
        
        # Source metadata expansion
        for source in result.get("sources", []):
            source["repository"] = request.repository
            
        result["status"] = "success"
        
        logging.info(f"Query completed in {result.get('total_time', 0):.3f}s")
        return QueryResponse(**result)
        
    except asyncio.TimeoutError:
        logging.error("Request timeout exceeded 15 seconds")
        return make_fallback_response(request.query, "The query request timed out. Please try again.", start_time)
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error executing query: {error_msg}")
        
        is_neo4j = any(kw in error_msg.lower() for kw in ["neo4j", "bolt", "connection", "reset", "closed", "10054", "7687"])
        if is_neo4j:
             return make_fallback_response(request.query, "The ACIS Knowledge Graph database is temporarily offline. Please ensure the Neo4j service is running and retry.", start_time)
        if "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
             return make_fallback_response(request.query, "The LLM API is temporarily unavailable due to rate limits. Please try again in a few moments.", start_time)
             
        return make_fallback_response(request.query, f"An internal error occurred during query execution: {error_msg}", start_time)

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
