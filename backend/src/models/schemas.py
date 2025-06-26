from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    source_documents: List[str]

class Document(BaseModel):
    id: str
    content: str
    metadata: dict

class DocumentResponse(BaseModel):
    documents: List[Document]