from pydantic import BaseModel, Field
from typing import List, Optional

class Source(BaseModel):
    entity_type: str
    entity_name: str
    repository: str
    score: Optional[float] = None

class QueryRequest(BaseModel):
    repository: str = Field(default="ACIS", description="The target repository to query.")
    query: str = Field(..., description="The natural language question to ask.")

class QueryResponse(BaseModel):
    query: str
    status: str = "success"
    answer: str
    sources: List[Source]
    retrieval_time: float
    generation_time: float
    total_time: float

class HealthResponse(BaseModel):
    status: str
    neo4j: str
    retriever: str
    llm: str
    repository: str
    version: str

class ErrorResponse(BaseModel):
    status: str = "error"
    success: bool = False
    error: str
