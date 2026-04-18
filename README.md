# RAG App

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?logo=fastapi&logoColor=white)
![Angular](https://img.shields.io/badge/Angular-latest-DD0031?logo=angular&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

Full-stack Retrieval-Augmented Generation application with FastAPI backend, Angular frontend, ChromaDB vector store, and PDF document ingestion.

## Architecture

```
Angular Frontend
        │
        ▼ (HTTP API)
┌──────────────────────────────┐
│  FastAPI Backend (:8000)     │
│                              │
│  PDF Upload ──► PyPDF2      │──► Text extraction
│       │                      │
│  Chunking ──► BeautifulSoup │──► Document processing
│       │                      │
│  Embedding ──► ChromaDB     │──► Vector storage & retrieval
│       │                      │
│  Generation ──► LLM         │──► Grounded answers
└──────────────────────────────┘
```

## Key Features

- **Document Ingestion** — Upload PDFs via the Angular UI, extracted with PyPDF2
- **Vector Storage** — ChromaDB for embedding storage and similarity search
- **RAG Pipeline** — Retrieve relevant chunks, generate grounded answers
- **Angular Frontend** — Modern SPA for document upload and Q&A
- **FastAPI Backend** — Async API with CORS support

## Quick Start

### Backend
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
ng serve
```

## Repository Structure

```
rag-app/
├── backend/
│   ├── src/
│   │   ├── main.py           # FastAPI entry point
│   │   └── api/
│   │       └── endpoints.py  # API routes
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/              # Angular components
│       └── main.ts           # Angular entry point
└── README.md
```

## License

MIT
# RAG App

Professional-grade full-stack Retrieval-Augmented Generation platform with FastAPI backend and Angular frontend.

## 1. Executive Overview

This repository provides:
- Document ingestion and retrieval pipeline
- Query answering through retrieval-augmented generation
- Full-stack developer workflow for backend and frontend

## 2. Architecture

```txt
Angular Frontend (4200)
        |
        v
FastAPI Backend (8000)
        |
        +--> Retrieval Layer
        +--> Vector Store (ChromaDB)
        +--> Model Runtime (Ollama)
```

## 3. Repository Structure

```txt
rag-app/
  backend/
    src/main.py
    requirements.txt
    chromadb/
  frontend/
    package.json
    src/
  README.md
```

## 4. Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- Ollama for local model runtime

## 5. Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 6. Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 7. Validation

```bash
cd backend
python3 -m compileall -q .
```

- Backend docs: http://127.0.0.1:8000/docs
- Frontend: http://localhost:4200

## 8. Troubleshooting

- API unavailable: verify backend process and port
- Frontend build errors: reinstall node modules
- Model runtime issues: ensure Ollama service is active

## 9. License

See LICENSE in this repository.
