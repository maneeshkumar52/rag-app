from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from pydantic import BaseModel
from src.services.rag_service import RAGService
import traceback

router = APIRouter()
rag_service = RAGService()

class QueryRequest(BaseModel):
    question: str
    technique: str = "basic"

class QueryResponse(BaseModel):
    answer: str
    documents: list = []

@router.post("/query", response_model=QueryResponse)
async def handle_query(
    request: Request,
    query: str = Form(None),
    technique: str = Form("basic")
):
    """
    Handles text-based queries with a selectable RAG technique.
    """
    try:
        # Try to get query from form or JSON body
        query_text = query
        if query_text is None:
            data = await request.json()
            query_text = data.get("query", "").strip()
            technique = data.get("technique", "basic")
        if not query_text:
            raise HTTPException(status_code=400, detail="No query provided.")
        result = rag_service.process_query(query_text, technique)
        return QueryResponse(answer=result["answer"], documents=result.get("documents", []))
    except Exception as e:
        print("Error during query:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query-file", response_model=QueryResponse)
async def handle_query_file(
    file: UploadFile = File(...),
    technique: str = Form("basic")
):
    """
    Handles file-based queries with a selectable RAG technique.
    """
    try:
        content = await file.read()
        query_text = content.decode("utf-8").strip()
        if not query_text:
            raise HTTPException(status_code=400, detail="No query provided in file.")
        result = rag_service.process_query(query_text, technique)
        return QueryResponse(answer=result["answer"], documents=result.get("documents", []))
    except Exception as e:
        print("Error during file query:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
      
@router.post("/ingest")
async def ingest_document(
    source_type: str = Form(...),
    file: UploadFile = File(None),
    url: str = Form(None)
):
    try:
        if source_type in ["text", "json", "pdf"] and file:
            file_path = f"/tmp/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(await file.read())
            rag_service.ingest_from_source(source_type, file_path)
        elif source_type == "web" and url:
            rag_service.ingest_from_source(source_type, url)
        else:
            raise HTTPException(status_code=400, detail="Invalid input")
        return {"status": "success"}
    except Exception as e:
        print("Error during ingestion:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))