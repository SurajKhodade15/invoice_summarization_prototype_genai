from typing import List, Any
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    source_documents: List[Any]

class UploadResponse(BaseModel):
    filename: str
    message: str
