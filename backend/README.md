# RAG App Backend

This is the backend for the RAG (Retrieval-Augmented Generation) application. It is built using FastAPI and serves as the API layer for the frontend Angular application. The backend handles document ingestion, storage, retrieval, and communication with the frontend.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [File and Component Explanations](#file-and-component-explanations)
- [Setup Instructions](#setup-instructions)
- [Running the Backend](#running-the-backend)
- [API Endpoints](#api-endpoints)
- [Sample Inputs](#sample-inputs)

---

## Prerequisites

Before running the backend, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **virtualenv** (recommended for isolated environments)
- **Ollama** (for running local LLMs)

### Installing Ollama

Ollama is required to run local large language models (LLMs) used by the backend for inference.

#### macOS

Download and install Ollama using Homebrew:

```sh
brew install ollama
```

Or download the installer from [https://ollama.com/download](https://ollama.com/download) and follow the installation instructions.

#### Windows

Download the Windows installer from [https://ollama.com/download](https://ollama.com/download) and run the installer.

#### Starting Ollama

After installation, start the Ollama service:

```sh
ollama serve
```

You may also need to pull a model (e.g., llama3):

```sh
ollama pull llama3
```

Make sure Ollama is running before starting the backend, as the backend will connect to it for LLM inference.

---

## Project Structure

```
backend/
├── README.md
├── requirements.txt
├── chromadb/
│   ├── chroma.sqlite3
│   └── <uuid>/
│       ├── data_level0.bin
│       └── header.bin
├── sample_inputs/
│   ├── meditations.pdf
│   ├── sample_query.txt
│   ├── sample.json
│   └── sample.txt
└── src/
    ├── main.py
    ├── api/
    ├── models/
    ├── services/
    └── utils/
```

---

## File and Component Explanations

### Top-Level Files

- **README.md**: This documentation file.
- **requirements.txt**: Lists all Python dependencies required to run the backend.
- **chromadb/**: Directory containing the ChromaDB vector database files for document storage and retrieval.
- **sample_inputs/**: Contains example files for testing ingestion and querying.

### `src/` Directory

- **main.py**: The entry point for the FastAPI application. It initializes the app, includes routers, and starts the server.
- **api/**: Contains FastAPI route definitions for various endpoints (e.g., document upload, query, health check).
- **models/**: Contains Pydantic models for request and response validation (e.g., schemas for queries, documents).
- **services/**: Contains business logic for document ingestion, retrieval, and interaction with ChromaDB.
- **utils/**: Utility functions for tasks such as file parsing, PDF extraction, and other helpers.

#### Details of Key Components

- **api/**
  - `__init__.py`: Initializes the API module.
  - `routes.py` (example): Defines API endpoints such as `/upload`, `/query`, etc.

- **models/**
  - `__init__.py`: Initializes the models module.
  - `document.py`: Pydantic model for document structure.
  - `query.py`: Pydantic model for query requests.

- **services/**
  - `__init__.py`: Initializes the services module.
  - `document_service.py`: Handles document ingestion, storage, and retrieval logic.
  - `query_service.py`: Handles query processing and retrieval-augmented generation logic.

- **utils/**
  - `__init__.py`: Initializes the utils module.
  - `pdf_parser.py`: Utility for extracting text from PDF files.
  - `file_utils.py`: Helpers for file operations.

---

## Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone <repository-url>
   cd backend
   ```

2. **Create and Activate a Virtual Environment (Recommended)**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

   This will install:
   - FastAPI (web framework)
   - chromadb (vector database)
   - uvicorn (ASGI server)
   - pydantic (data validation)
   - httpx (HTTP client)
   - python-dotenv (environment variable management)
   - PyPDF2 (PDF parsing)
   - python-multipart (file upload support)

4. **Prepare ChromaDB**

   - The `chromadb/` directory is pre-populated with a SQLite database and binary files for vector storage.
   - No manual setup is required unless you want to reset or migrate the database.

5. **(Optional) Add Environment Variables**

   - If your application uses environment variables, create a `.env` file in the `backend/` directory and add your variables there.

---

## Running the Backend

1. **Start Ollama**

   Make sure Ollama is running:
   ```sh
   ollama serve
   ```

2. **Start the FastAPI Server**

   ```sh
   cd src
   uvicorn src.main:app --reload
   ```

   - The `--reload` flag enables auto-reloading on code changes (useful for development).
   - By default, the server runs at `http://127.0.0.1:8000`.

3. **Access the API Docs**

   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

---

## API Endpoints

- **POST /upload**: Upload a document (PDF or text) for ingestion.
- **POST /query**: Submit a query and receive a retrieval-augmented response.
- **GET /health**: Health check endpoint.

*See the Swagger UI for detailed request/response schemas.*

---

## Sample Inputs

The `sample_inputs/` directory contains:

- `meditations.pdf`: Example PDF for ingestion.
- `sample_query.txt`: Example query text file.
- `sample.json`: Example JSON input.
- `sample.txt`: Example plain text file.

Use these files to test the ingestion and querying endpoints.

---

## Advanced RAG Techniques

The frontend supports advanced RAG techniques. When submitting a query, users can select the retrieval strategy:
- **Basic**: Standard retrieval-augmented generation.
- **Hybrid Search**: Combines keyword and semantic search.
- **Reranking**: Retrieves candidates and reranks them using a secondary model.
- **Semantic Search**: Uses embeddings for retrieval.

The selected technique is sent to the backend, which must support the `technique` parameter in the `/query` endpoint.

---