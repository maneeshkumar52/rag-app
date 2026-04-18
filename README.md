<div align="center">

# 📚 RAG App — Local Retrieval-Augmented Generation System

**A privacy-first, self-hosted RAG application that lets you ingest documents (PDF, text, JSON, web pages) into a ChromaDB vector store and query them conversationally through a local Mistral LLM via Ollama — no cloud AI APIs required.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Angular](https://img.shields.io/badge/Angular-13-DD0031?logo=angular&logoColor=white)](https://angular.io)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00)](https://www.trychroma.com)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral_LLM-000000)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Project Structure](#-project-structure) · [Configuration](#-configuration-reference) · [Troubleshooting](#-troubleshooting)

</div>

---

## 🎯 What This Project Does

RAG App is a **complete full-stack Retrieval-Augmented Generation system** designed for local, privacy-friendly document intelligence. Upload your proprietary documents — PDFs, text files, JSON data, or web pages — and ask natural language questions. The system retrieves relevant context from the ChromaDB vector store and generates grounded answers using a locally running Mistral model through Ollama.

### The Problem It Solves

| Challenge | RAG App Solution |
|---|---|
| Cloud AI APIs expose sensitive data | Runs entirely locally — documents never leave your machine |
| RAG pipelines require complex setup | Two-service architecture: FastAPI backend + Angular frontend |
| Multiple document formats | Unified ingestion for PDF, text, JSON, and web pages |
| Black-box AI responses | Answers include source documents for verification |
| Expensive API costs | Free local inference via Ollama + Mistral |

### Key Differentiators

- **Zero cloud dependencies** — All inference happens locally via Ollama
- **Multi-format ingestion** — PDF (PyPDF2), text, JSON, web scraping (BeautifulSoup)
- **Technique selector** — Switch between RAG retrieval strategies at query time
- **Source transparency** — Every answer includes the retrieved documents that informed it
- **Embedded vector store** — ChromaDB with `all-MiniLM-L6-v2` embeddings, no external DB server needed

---

## ✨ Features

| Feature | Description | Status |
|---|---|---|
| PDF Document Ingestion | Extract and index text from PDF files via PyPDF2 | ✅ Working |
| Text File Ingestion | Ingest plain text documents directly | ✅ Working |
| JSON File Ingestion | Parse and index structured JSON data | ✅ Working |
| Web Page Ingestion | Scrape and index content from URLs via BeautifulSoup | ✅ Working |
| Basic RAG Query | Similarity search + LLM generation | ✅ Working |
| Hybrid RAG Query | Combined keyword + semantic retrieval | ⚠️ Stub only |
| Reranking RAG Query | Cross-encoder reranking of results | ⚠️ Stub only |
| Semantic RAG Query | Pure semantic embedding search | ⚠️ Stub only |
| File-Based Query | Upload a text file containing your question | ✅ Working |
| Chat Interface | Conversational UI with message history | ✅ Working |
| Source Documents | View retrieved context alongside answers | ✅ Working |
| Responsive Design | Mobile-friendly card-based layout | ✅ Working |

---

## 🏗 Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────┐
│                Angular Frontend (:4200)                    │
│                                                            │
│  ┌────────────┐    ┌────────────────────────────────┐    │
│  │ AppComponent│───▶│     RagChatComponent            │    │
│  └────────────┘    │                                  │    │
│                    │  ┌──────────┐  ┌─────────────┐  │    │
│                    │  │ Ingest   │  │ Chat Panel   │  │    │
│                    │  │ Panel    │  │ + Technique  │  │    │
│                    │  │          │  │   Selector   │  │    │
│                    │  └──────────┘  └─────────────┘  │    │
│                    └──────────────┬───────────────────┘    │
│                                   │                        │
│  ┌────────────────────────────────▼───────────────────┐   │
│  │              RagService (HttpClient)                │   │
│  │   POST /query  │  POST /query-file  │  POST /ingest│   │
│  └────────────────────────────────┬───────────────────┘   │
└───────────────────────────────────┼────────────────────────┘
                                    │ HTTP (JSON / FormData)
┌───────────────────────────────────▼────────────────────────┐
│                FastAPI Backend (:8000)                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  endpoints.py (APIRouter)                            │   │
│  │  POST /query      — text query + technique selector  │   │
│  │  POST /query-file — file-based query                 │   │
│  │  POST /ingest     — document ingestion               │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                          │                                  │
│  ┌───────────────────────▼──────────────────────────────┐  │
│  │  RAGService (orchestrator)                            │  │
│  │  ingest_from_source() → document loaders              │  │
│  │  process_query()      → retrieve + generate           │  │
│  └─────┬──────────────────────────────┬─────────────────┘  │
│        │                              │                     │
│  ┌─────▼──────────────┐  ┌───────────▼──────────────┐     │
│  │  ChromaDBClient     │  │    OllamaClient           │     │
│  │  (vector store)     │  │    (LLM generation)       │     │
│  │  PersistentClient   │  │    POST /api/generate     │     │
│  └─────┬──────────────┘  └───────────┬──────────────┘     │
│        │                              │                     │
│  ┌─────▼──────────────┐  ┌───────────▼──────────────┐     │
│  │  ./chromadb/        │  │  localhost:11434          │     │
│  │  (SQLite + bins)    │  │  (Ollama / Mistral)      │     │
│  └────────────────────┘  └──────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow — Query Pipeline

```
User types question in Angular chat
        │
        ▼
RagChatComponent.sendMessage()
        │
        ▼
RagService.sendQuery(question, technique)
        │
        ▼  POST /query  {query, technique}
endpoints.py → handle_query()
        │
        ▼
RAGService.process_query(query, technique)
        │
        ├─── technique == "basic" ──▶ ChromaDBClient.retrieve_documents(query)
        │                                   │
        │                                   ▼
        │                            ChromaDB similarity search
        │                            (all-MiniLM-L6-v2 embeddings)
        │                            Returns top 2 documents
        │                                   │
        ▼                                   │
Prompt Construction ◀───────────────────────┘
        │
        │   "Context:\n{doc1}\n{doc2}\n\nQuestion: {query}\nAnswer:"
        │
        ▼
OllamaClient.generate_response(prompt)
        │
        ▼  POST http://localhost:11434/api/generate
Ollama / Mistral generates answer
        │
        ▼
Response: {answer: "...", documents: [...]}
        │
        ▼
Angular displays answer + source docs in chat
```

### Data Flow — Ingestion Pipeline

```
User selects source type (text/json/pdf/web)
        │
        ├── File selected → FormData with file
        │── URL entered   → FormData with url string
        │
        ▼  POST /ingest
endpoints.py → ingest_document()
        │
        ├── File → saved to /tmp/{filename}
        │── URL  → passed directly
        │
        ▼
RAGService.ingest_from_source(source_type, path)
        │
        ├── "text" → load_text_file()    → plain read
        ├── "json" → load_json_file()    → JSON parse + dumps
        ├── "pdf"  → load_pdf_file()     → PyPDF2 page extraction
        └── "web"  → load_web_content()  → requests + BeautifulSoup
                │
                ▼
ChromaDBClient.ingest_document(collection, content, metadata)
        │
        ▼
ChromaDB generates embedding (all-MiniLM-L6-v2)
Stores: {id: UUID4, document: text, metadata: {source, type}}
```

---

## 🧠 RAG Pipeline Design

### Retrieval Strategy

| Decision | Choice | Rationale |
|---|---|---|
| Vector Store | ChromaDB (embedded) | Zero-config, file-based persistence, built-in embeddings |
| Embedding Model | all-MiniLM-L6-v2 | ChromaDB default, good quality-speed tradeoff |
| Retrieval Count | 2 documents | Minimizes prompt size for small local LLM context |
| Chunking Strategy | None (whole document) | Simple ingestion, trades retrieval granularity for simplicity |
| LLM Provider | Ollama (local) | Privacy-first, no API keys required |
| LLM Model | Mistral | Good instruction-following, runs on consumer hardware |
| Prompt Template | Zero-shot context+question | Minimal prompt — no system instruction or few-shot examples |
| Streaming | Disabled | Simpler response handling, full response returned |

### Prompt Template

The system uses a single, minimal prompt template for all queries:

```
Context:
{retrieved_document_1}
{retrieved_document_2}

Question: {user_query}
Answer:
```

**Design characteristics:**
- No system prompt or persona instruction
- No few-shot examples or chain-of-thought guidance
- No output format specification
- Context is raw concatenation of retrieved documents
- Relies entirely on the LLM's instruction-following capability

### RAG Technique Comparison

| Technique | Method Called | Status | Description |
|---|---|---|---|
| `basic` | `retrieve_documents()` | ✅ Implemented | Standard cosine similarity search via ChromaDB |
| `hybrid` | `retrieve_documents_hybrid()` | ⚠️ Not implemented | Would combine keyword + semantic search |
| `reranking` | `retrieve_documents_reranking()` | ⚠️ Not implemented | Would use cross-encoder to re-score results |
| `semantic` | `retrieve_documents_semantic()` | ⚠️ Not implemented | Would use enhanced semantic matching |

> **Note:** Only `basic` is functional. The other techniques are exposed in the UI but will raise `AttributeError` at runtime. This is an intentional roadmap — the architecture supports plugging in additional retrieval methods.

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Installation |
|---|---|---|
| Python | 3.9+ | [python.org](https://python.org) |
| Node.js | 14+ | [nodejs.org](https://nodejs.org) |
| Angular CLI | ~13.0 | `npm install -g @angular/cli@13` |
| Ollama | Latest | [ollama.com](https://ollama.com) |

### Step 1: Clone and Navigate

```bash
git clone https://github.com/maneeshkumar52/rag-app.git
cd rag-app
```

### Step 2: Start Ollama and Pull Model

```bash
# Start the Ollama runtime (runs on localhost:11434)
ollama serve

# In another terminal, pull the Mistral model (~4.1 GB)
ollama pull mistral
```

<details>
<summary>📋 Expected Output — Ollama Setup</summary>

```
$ ollama serve
time=2024-01-15T10:30:00.000Z level=INFO source=serve.go msg="starting ollama" version=0.1.x
time=2024-01-15T10:30:00.100Z level=INFO source=serve.go msg="listening on 127.0.0.1:11434"

$ ollama pull mistral
pulling manifest
pulling e8a35b5937a5... 100% ▕████████████████████████████████▏ 4.1 GB
pulling 43070e2d4e53... 100% ▕████████████████████████████████▏  11 KB
pulling e6836092461f... 100% ▕████████████████████████████████▏   42 B
pulling ed11eda7790d... 100% ▕████████████████████████████████▏   30 B
pulling f9b1e3196ecf... 100% ▕████████████████████████████████▏  483 B
verifying sha256 digest
writing manifest
removing any unused layers
success
```

</details>

### Step 3: Set Up Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

<details>
<summary>📋 Expected Output — Backend Setup</summary>

```
$ pip install -r requirements.txt
Collecting FastAPI
  Downloading fastapi-0.109.2-py3-none-any.whl (92 kB)
Collecting chromadb
  Downloading chromadb-0.4.22-py3-none-any.whl (502 kB)
Collecting uvicorn
  Downloading uvicorn-0.27.0-py3-none-any.whl (60 kB)
Collecting pydantic
  Downloading pydantic-2.6.1-py3-none-any.whl (394 kB)
Collecting PyPDF2
  Downloading PyPDF2-3.0.1-py3-none-any.whl (232 kB)
Collecting beautifulsoup4
  Downloading beautifulsoup4-4.12.3-py3-none-any.whl (147 kB)
...
Successfully installed FastAPI-0.109.2 chromadb-0.4.22 uvicorn-0.27.0 ...
```

</details>

### Step 4: Start Backend

```bash
# From backend/ directory
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

<details>
<summary>📋 Expected Output — Backend Running</summary>

```
$ uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
INFO:     Will watch for changes in these directories: ['/path/to/rag-app/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</details>

### Step 5: Set Up and Start Frontend

```bash
# Open new terminal
cd frontend
npm install
ng serve
```

<details>
<summary>📋 Expected Output — Frontend Running</summary>

```
$ ng serve
✔ Browser application bundle generation complete.

Initial Chunk Files | Names         |  Raw Size
vendor.js           | vendor        | 2.07 MB |
polyfills.js        | polyfills     | 128.54 kB |
main.js             | main          |  15.23 kB |
styles.css          | styles        |   0.14 kB |
runtime.js          | runtime       |   6.52 kB |

** Angular Live Development Server is listening on localhost:4200 **

✔ Compiled successfully.
```

</details>

### Step 6: Use the Application

1. Open **http://localhost:4200** in your browser
2. **Ingest a document:** Select source type → Upload file or enter URL → Click "Ingest"
3. **Ask a question:** Type in the chat box → Select RAG technique (use "basic") → Send

### Quick Test with Sample Data

```bash
# Ingest the provided sample text file
curl -X POST http://localhost:8000/ingest \
  -F "source_type=text" \
  -F "file=@backend/sample_inputs/sample.txt"

# Query against ingested content
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What advice does Marcus Aurelius give for dealing with adversity?", "technique": "basic"}'
```

<details>
<summary>📋 Expected Output — Sample Query</summary>

```json
{
  "answer": "Marcus Aurelius advises that when facing adversity, one should focus on what is within their control. In Book 5, he writes about accepting difficulties as natural and using them as opportunities for growth. He emphasizes that our perception of events matters more than the events themselves, and encourages maintaining inner tranquility regardless of external circumstances.",
  "documents": [
    {
      "content": "Book 5, Meditation 20: Think of yourself as dead. You have lived your life. Now, take what's left and live it properly..."
    },
    {
      "content": "Book 4, Meditation 3: People seek retreats for themselves in the countryside..."
    }
  ]
}
```

</details>

---

## 📡 API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

#### `POST /query` — Text Query

Send a natural language question and receive an AI-generated answer grounded in retrieved documents.

**Request (JSON):**
```json
{
  "query": "What is the main theme of the text?",
  "technique": "basic"
}
```

**Request (FormData alternative):**
```
query=What+is+the+main+theme    (Form field)
technique=basic                  (Form field)
```

**Response:**
```json
{
  "answer": "The main theme revolves around Stoic philosophy...",
  "documents": [
    {"content": "Retrieved document text..."},
    {"content": "Second retrieved document..."}
  ]
}
```

| Status | Meaning |
|---|---|
| `200` | Success — answer generated |
| `400` | No query provided |
| `404` | No relevant documents found in vector store |
| `500` | Internal error (Ollama unreachable, ChromaDB error) |

---

#### `POST /query-file` — File-Based Query

Upload a text file containing your question.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | File | ✅ | Text file with query text |
| `technique` | string | ❌ | RAG technique (default: `basic`) |

**Response:** Same schema as `/query`

---

#### `POST /ingest` — Document Ingestion

Ingest a document into the ChromaDB vector store.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `source_type` | string | ✅ | `text`, `json`, `pdf`, or `web` |
| `file` | File | Conditional | Required for text/json/pdf source types |
| `url` | string | Conditional | Required for web source type |

**Response:**
```json
{"status": "success"}
```

**Supported Document Formats:**

| Format | Handler | What It Does |
|---|---|---|
| `text` | `load_text_file()` | Reads file as plain text |
| `json` | `load_json_file()` | Parses JSON, re-serializes as string |
| `pdf` | `load_pdf_file()` | Extracts text from all pages via PyPDF2 |
| `web` | `load_web_content()` | Fetches URL, strips HTML tags with BeautifulSoup |

---

## 📂 Project Structure

```
rag-app/
├── backend/
│   ├── requirements.txt                    # Python dependencies (unpinned)
│   ├── README.md                           # Backend-specific documentation
│   ├── chromadb/                           # Vector store data (auto-created)
│   │   ├── chroma.sqlite3                  # Metadata database
│   │   └── {uuid}/                         # Embedding binary data
│   ├── sample_inputs/                      # Test documents
│   │   ├── sample.txt                      # Marcus Aurelius excerpts (text)
│   │   ├── sample.json                     # Same content in JSON format
│   │   ├── sample_query.txt                # Example query file
│   │   └── meidtations.pdf                 # Meditations PDF
│   └── src/
│       ├── main.py                         # FastAPI app entry point
│       ├── api/
│       │   └── endpoints.py                # Route definitions (3 endpoints)
│       ├── models/
│       │   └── schemas.py                  # Pydantic models (unused)
│       ├── services/
│       │   ├── chromadb_client.py           # Vector store wrapper
│       │   ├── ollama_client.py             # LLM client wrapper
│       │   └── rag_service.py              # Core RAG orchestrator
│       └── utils/
│           ├── document_loaders.py          # PDF/text/JSON/web parsers
│           └── helpers.py                   # Utility functions (unused)
│
├── frontend/
│   ├── angular.json                        # Angular workspace config
│   ├── package.json                        # Node.js dependencies
│   ├── tsconfig.json                       # TypeScript configuration
│   └── src/
│       ├── index.html                      # SPA entry point
│       ├── main.ts                         # Angular bootstrap
│       ├── styles.css                      # Global styles
│       └── app/
│           ├── app.module.ts               # Root module
│           ├── app.component.ts            # Root component → delegates to RagChat
│           ├── components/
│           │   └── rag-chat/
│           │       ├── rag-chat.component.ts    # Main UI logic (102 lines)
│           │       ├── rag-chat.component.html  # Template (65 lines)
│           │       └── rag-chat.component.css   # Card-based layout (169 lines)
│           └── services/
│               └── rag.service.ts          # HTTP service for backend API
│
└── .gitignore
```

### Module Responsibility Map

| Module | Role | Lines | Key Exports |
|---|---|---|---|
| `main.py` | App creation, CORS, router mount | 20 | `app` (FastAPI) |
| `endpoints.py` | HTTP route handlers | 81 | `router`, `handle_query()`, `ingest_document()` |
| `rag_service.py` | Business logic orchestrator | 46 | `RAGService` class |
| `chromadb_client.py` | Vector store abstraction | 43 | `ChromaDBClient` class |
| `ollama_client.py` | LLM API wrapper | 13 | `OllamaClient` class |
| `document_loaders.py` | Format-specific parsers | 38 | `load_text_file()`, `load_pdf_file()`, etc. |
| `rag.service.ts` | Frontend HTTP client | 34 | `RagService` class |
| `rag-chat.component.ts` | Chat UI logic | 102 | `RagChatComponent` class |

---

## 🗄 Data Models

### ChromaDB Document Schema

Each ingested document is stored in the `default` collection:

```
┌─────────────────────────────────────────────────┐
│  ChromaDB Collection: "default"                  │
├──────────┬──────────────────────────────────────┤
│ Field    │ Description                           │
├──────────┼──────────────────────────────────────┤
│ id       │ UUID4 string (auto-generated)         │
│ document │ Raw text content (full document)      │
│ metadata │ {source: filepath/url, type: format}  │
│ embedding│ all-MiniLM-L6-v2 vector (auto)       │
└──────────┴──────────────────────────────────────┘
```

### API Response Models

```python
# QueryResponse — returned by /query and /query-file
{
    "answer": str,       # LLM-generated answer
    "documents": [       # Retrieved source documents
        {"content": str}
    ]
}

# IngestResponse — returned by /ingest
{
    "status": "success"
}
```

### Pydantic Models (endpoints.py — actually used)

```python
class QueryRequest(BaseModel):     # Defined but NOT used as endpoint parameter
    question: str
    technique: str = "basic"

class QueryResponse(BaseModel):    # Used as response_model
    answer: str
    documents: list = []
```

---

## ⚙️ Configuration Reference

### Backend Configuration

All configuration is currently hardcoded. No environment variables are read despite `python-dotenv` being imported.

| Setting | Value | Location | Description |
|---|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | `ollama_client.py` | Ollama API endpoint |
| `OLLAMA_MODEL` | `mistral` | `ollama_client.py` | LLM model for generation |
| `CHROMADB_PATH` | `./chromadb` | `rag_service.py` | Vector store directory |
| `COLLECTION_NAME` | `default` | `rag_service.py` | ChromaDB collection name |
| `N_RESULTS` | `2` | `chromadb_client.py` | Documents retrieved per query |
| `CORS_ORIGINS` | `["*"]` | `main.py` | Allowed CORS origins |
| `HOST` | `0.0.0.0` | `main.py` | Server bind address |
| `PORT` | `8000` | `main.py` | Server HTTP port |
| `TEMP_DIR` | `/tmp/` | `endpoints.py` | Uploaded file staging |

### Frontend Configuration

| Setting | Value | Location | Description |
|---|---|---|---|
| `API_URL` | `http://localhost:8000` | `rag.service.ts` | Backend API base URL |
| `DEV_PORT` | `4200` | `angular.json` | Angular dev server port |
| `BUILD_OUTPUT` | `dist/rag-app` | `angular.json` | Production build directory |
| `TS_TARGET` | `es2015` | `tsconfig.json` | TypeScript compilation target |

### Making Configuration Dynamic

To externalize configuration, add a `.env` file (the `load_dotenv()` call already exists):

```bash
# backend/.env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
CHROMADB_PATH=./chromadb
COLLECTION_NAME=default
```

Then update the service constructors to read from `os.getenv()`.

---

## 🧪 Sample Data

The repository includes sample documents for testing:

### `backend/sample_inputs/sample.txt`
Seven passages from Marcus Aurelius' *Meditations* covering Stoic philosophy themes:
- Resilience and adversity (Books 2, 5)
- Self-focus and inner peace (Book 4)
- Purpose and duty (Book 6)
- Truth-seeking (Books 7, 8, 10)

### `backend/sample_inputs/sample.json`
The same seven meditations in structured JSON format with book number, meditation number, text, and summary fields.

### `backend/sample_inputs/sample_query.txt`
Pre-written query: *"What advice does Marcus Aurelius give for dealing with adversity?"*

### `backend/sample_inputs/meidtations.pdf`
PDF version of the Meditations content.

---

## 🔧 Design Decisions

### Why These Choices Were Made

| Decision | Alternatives Considered | Rationale |
|---|---|---|
| **ChromaDB (embedded)** vs. Pinecone, Weaviate, FAISS | Cloud vector DBs add latency and cost; FAISS lacks persistence | Zero-config, file-persisted, built-in embedding function |
| **Ollama (local)** vs. OpenAI, Anthropic APIs | Cloud APIs expose data, require keys, incur costs | Privacy-first, free inference, runs on consumer hardware |
| **Mistral** vs. Llama2, CodeLlama, Phi-2 | Llama2 is larger; Phi-2 is less capable for QA | Best instruction-following at 7B parameter size |
| **FastAPI** vs. Flask, Django | Flask lacks async; Django is heavy for API-only | Native async, auto OpenAPI docs, Pydantic validation |
| **Angular 13** vs. React, Vue, Svelte | React would work equally well | Component architecture, built-in HTTP client, TypeScript-first |
| **No chunking** vs. RecursiveCharacterTextSplitter | Chunking adds complexity for a demo app | Simplicity — suitable for small documents |
| **2 results** vs. 3-5 typical RAG | More results increase prompt size | Keeps prompt within Mistral's effective context range |
| **Module-level singleton** vs. dependency injection | DI is more testable | Simple, no FastAPI dependency injection overhead |

### Architectural Tradeoffs

```
Simplicity ◀──────────────────────────────────▶ Production-Readiness

This project optimizes for:
  ✅ Easy to understand          ❌ No authentication
  ✅ Easy to run locally         ❌ No chunking strategy
  ✅ Minimal dependencies        ❌ No conversation memory
  ✅ Clear separation of concerns ❌ No structured logging
  ✅ Self-contained (no cloud)   ❌ No Docker deployment
```

---

## 🐛 Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---|---|---|
| `ConnectionRefusedError` on query | Ollama not running | Start Ollama: `ollama serve` |
| `model 'mistral' not found` | Model not pulled | Pull model: `ollama pull mistral` |
| `No relevant documents found` | Empty vector store | Ingest documents first via `/ingest` |
| `AttributeError: retrieve_documents_hybrid` | Non-basic technique selected | Use `technique: "basic"` only |
| Frontend can't reach backend | CORS or port mismatch | Verify backend runs on `:8000`, check CORS config |
| `ModuleNotFoundError: PyPDF2` | Dependencies not installed | `pip install -r requirements.txt` |
| ChromaDB permission error | DB locked by another process | Stop other backend instances, delete `chromadb/` to reset |
| Slow first query | Model loading into memory | First query loads Mistral (~4GB RAM); subsequent queries are fast |
| `ng: command not found` | Angular CLI not installed | `npm install -g @angular/cli@13` |
| Large PDF ingestion fails | No chunking — single huge document | Split large PDFs into smaller files before ingestion |

### Verifying Services Are Running

```bash
# Check Ollama
curl http://localhost:11434/api/tags
# Expected: {"models": [{"name": "mistral:latest", ...}]}

# Check Backend
curl http://localhost:8000/docs
# Expected: FastAPI Swagger UI (redirects to /docs)

# Check Frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200
# Expected: 200
```

### Resetting the Vector Store

```bash
# Delete all ingested documents and start fresh
rm -rf backend/chromadb/
# Restart the backend — ChromaDB recreates the directory automatically
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)

| Package | Purpose | Used In |
|---|---|---|
| `FastAPI` | Async web framework, OpenAPI docs | `main.py`, `endpoints.py` |
| `chromadb` | Embedded vector database | `chromadb_client.py` |
| `uvicorn` | ASGI server | `main.py` |
| `pydantic` | Request/response validation | `endpoints.py` |
| `httpx` | Async HTTP client | **Not used in code** |
| `python-dotenv` | `.env` file loading | `main.py` (loaded but no vars read) |
| `PyPDF2` | PDF text extraction | `document_loaders.py` |
| `python-multipart` | File upload support | `endpoints.py` |
| `beautifulsoup4` | HTML parsing for web scraping | `document_loaders.py` |
| `requests` | HTTP client (implicit) | `ollama_client.py`, `document_loaders.py` |

### Frontend (`package.json`)

| Package | Version | Purpose |
|---|---|---|
| `@angular/core` | ~13.0.0 | Component model, DI, lifecycle hooks |
| `@angular/common` | ~13.0.0 | NgIf, NgFor, NgClass directives |
| `@angular/forms` | ~13.0.0 | Template-driven forms (ngModel) |
| `@angular/router` | ~13.0.0 | Routing (imported but unused) |
| `rxjs` | ~6.5.5 | Reactive programming, Observables |
| `zone.js` | ~0.11.4 | Angular change detection |
| `typescript` | ~4.4.4 | TypeScript compiler |

---

## 🔒 Security Considerations

This application is designed for **local development only**. The following security aspects should be addressed before any network exposure:

| Area | Current State | Recommendation |
|---|---|---|
| Authentication | None — all endpoints public | Add API key or JWT authentication |
| CORS | `allow_origins=["*"]` | Restrict to specific frontend origin |
| Input Validation | Basic empty-check only | Add length limits, sanitize file names |
| Web Ingestion | Fetches any URL (SSRF risk) | Allowlist domains, block internal IPs |
| File Upload | Saves to `/tmp/{filename}` | Sanitize filenames, use temp directory with random names |
| Rate Limiting | None | Add rate limiting middleware |
| HTTPS | Not configured | Use reverse proxy with TLS for network access |
| Dependency Versions | Unpinned | Pin all versions in `requirements.txt` |

---

## ☁️ Azure Production Mapping

For deploying this RAG application to Azure with production-grade infrastructure:

| Local Component | Azure Service | Configuration |
|---|---|---|
| FastAPI Backend | **Azure Container Apps** | 1 vCPU, 2 GiB RAM, HTTP ingress on port 8000 |
| Angular Frontend | **Azure Static Web Apps** | Free tier, auto-build from GitHub |
| Ollama + Mistral | **Azure OpenAI Service** | GPT-4o or GPT-3.5-turbo deployment |
| ChromaDB (embedded) | **Azure AI Search** | Basic tier, vector search enabled |
| `/tmp/` file staging | **Azure Blob Storage** | Standard tier, private container |
| No auth → | **Azure Entra ID** | MSAL.js + FastAPI middleware |
| No monitoring → | **Azure Application Insights** | Python + Angular SDKs |
| No secrets management → | **Azure Key Vault** | Store API keys, connection strings |

### Deployment Architecture

```
                    ┌──────────────────┐
                    │  Azure Front Door │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │                             │
    ┌─────────▼──────────┐     ┌───────────▼──────────┐
    │  Azure Static       │     │  Azure Container      │
    │  Web Apps           │     │  Apps                  │
    │  (Angular Frontend) │────▶│  (FastAPI Backend)     │
    └────────────────────┘     └───┬──────────┬────────┘
                                    │          │
                          ┌────────▼──┐  ┌───▼──────────┐
                          │ Azure AI   │  │ Azure Blob    │
                          │ Search     │  │ Storage       │
                          │ (vectors)  │  │ (documents)   │
                          └────────────┘  └──────────────┘
                                    │
                          ┌────────▼──────────┐
                          │  Azure OpenAI      │
                          │  (GPT-4o)          │
                          └───────────────────┘
```

### Cost Estimation (Monthly)

| Service | Tier | Estimated Cost |
|---|---|---|
| Container Apps | Consumption | ~$5-15 |
| Static Web Apps | Free | $0 |
| Azure AI Search | Basic | ~$70 |
| Azure OpenAI | Pay-per-token | ~$10-50 (varies by usage) |
| Blob Storage | Standard | ~$1-5 |
| **Total** | | **~$86-140/month** |

---

## 🚀 Production Checklist

Before deploying to any environment beyond local development:

- [ ] Pin all Python dependency versions in `requirements.txt`
- [ ] Add authentication (API keys or OAuth2)
- [ ] Restrict CORS to specific frontend origin
- [ ] Implement document chunking (RecursiveCharacterTextSplitter)
- [ ] Increase retrieval count from 2 to 3-5
- [ ] Add system prompt with persona and output format instructions
- [ ] Implement conversation memory for multi-turn context
- [ ] Add structured logging (replace `print()` with `logging`)
- [ ] Sanitize uploaded filenames and validate file types
- [ ] Block SSRF in web ingestion (allowlist domains, block RFC 1918 IPs)
- [ ] Add input length limits on queries and documents
- [ ] Add rate limiting middleware
- [ ] Create Dockerfile and docker-compose.yml
- [ ] Implement the hybrid/reranking/semantic retrieval methods or remove from UI
- [ ] Add health check endpoint (`GET /health`)
- [ ] Remove dead code (`schemas.py`, `helpers.py`)
- [ ] Add test suite (pytest for backend, Karma/Jasmine for frontend)
- [ ] Externalize configuration to environment variables
- [ ] Set up CI/CD pipeline

---

## 📄 License

This project is available under the MIT License.

---

<div align="center">

**Built with FastAPI · Angular · ChromaDB · Ollama**

*A self-hosted RAG system for private document intelligence*

</div>