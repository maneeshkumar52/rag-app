from fastapi import HTTPException
from typing import Any, Dict
from src.services.chromadb_client import ChromaDBClient
from src.utils.document_loaders import load_text_file, load_json_file, load_pdf_file, load_web_content
import os
from .ollama_client import OllamaClient

class RAGService:
    def __init__(self):
        self.chromadb_client = ChromaDBClient(db_url="./chromadb")
        self.ollama_client = OllamaClient()
        
    def ingest_from_source(self, source_type: str, source_path: str, collection_name: str = "default"):
        if source_type == "text":
            content = load_text_file(source_path)
        elif source_type == "json":
            content = load_json_file(source_path)
        elif source_type == "pdf":
            content = load_pdf_file(source_path)
        elif source_type == "web":
            content = load_web_content(source_path)
        else:
            raise ValueError("Unsupported source type")
        self.chromadb_client.ingest_document(collection_name, content, metadata={"source": source_path, "type": source_type})

    def process_query(self, query: str, technique: str = "basic") -> Dict[str, Any]:
        # Use the technique parameter to select the retrieval strategy
        if technique == "basic":
            documents = self.chromadb_client.retrieve_documents(query)
        elif technique == "hybrid":
            documents = self.chromadb_client.retrieve_documents_hybrid(query)
        elif technique == "reranking":
            documents = self.chromadb_client.retrieve_documents_reranking(query)
        elif technique == "semantic":
            documents = self.chromadb_client.retrieve_documents_semantic(query)
        else:
            raise HTTPException(status_code=400, detail="Unknown RAG technique")

        if not documents:
            raise HTTPException(status_code=404, detail="No relevant documents found.")
        context = "\n".join([doc["content"] for doc in documents])
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        response = self.ollama_client.generate_response(prompt)
        return {
            "answer": response,
            "documents": documents
        }