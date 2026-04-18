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
