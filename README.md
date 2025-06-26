# RAG App (Retrieval-Augmented Generation)

This repository contains a full-stack Retrieval-Augmented Generation (RAG) application. The backend is built with FastAPI and integrates with ChromaDB and Ollama for LLM inference and vector storage. The frontend is built with Angular and provides a user-friendly interface for document upload, querying, and viewing responses.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Sample Inputs](#sample-inputs)
- [Advanced RAG Techniques](#advanced-rag-techniques)
- [Available Scripts](#available-scripts)
- [Implementation Overview](#implementation-overview)

---

## Features

- **Document Upload:** Upload PDF or text files for ingestion and retrieval.
- **Query Submission:** Submit queries and receive retrieval-augmented responses.
- **Advanced Retrieval:** Supports hybrid, reranking, and semantic search strategies.
- **Interactive UI:** Angular-based frontend for seamless user experience.
- **API Documentation:** Swagger UI for backend API exploration.

---

## Project Structure

```
.
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── chromadb/
│   ├── sample_inputs/
│   └── src/
│       ├── main.py
│       ├── api/
│       ├── models/
│       ├── services/
│       └── utils/
└── frontend/
    ├── README.md
    ├── angular.json
    ├── package.json
    ├── tsconfig.json
    └── src/
        ├── index.html
        ├── main.ts
        ├── polyfills.ts
        ├── styles.css
        └── app/
```

---

## Prerequisites

### Backend

- **Python 3.8+**
- **pip**
- **virtualenv** (recommended)
- **Ollama** (for local LLMs)
- **ChromaDB** (included as files)

### Frontend

- **Node.js** (v14+)
- **npm**
- **Angular CLI** (v13.x)

---

## Setup Instructions

### Backend

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd backend
   ```

2. **Create and Activate a Virtual Environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install Ollama**
   - macOS: `brew install ollama` or download from [https://ollama.com/download](https://ollama.com/download)
   - Windows: Download and install from [https://ollama.com/download](https://ollama.com/download)
   - Start Ollama: `ollama serve`
   - Pull a model: `ollama pull llama3`

5. **Prepare ChromaDB**
   - The `chromadb/` directory is pre-populated. No manual setup required.

6. **(Optional) Add Environment Variables**
   - Create a `.env` file in `backend/` if needed.

---

### Frontend

1. **Clone the Repository**
   ```sh
   cd frontend
   ```

2. **Install Dependencies**
   ```sh
   npm install
   ```

3. **Install Angular CLI (if not already)**
   ```sh
   npm install -g @angular/cli@13
   ```

---

## Running the Application

### Backend

1. **Start Ollama**
   ```sh
   ollama serve
   ```

2. **Start FastAPI Server**
   ```sh
   cd backend/src
   uvicorn src.main:app --reload
   ```
   - API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Frontend

1. **Start Angular Development Server**
   ```sh
   cd frontend
   npm start
   ```
   or
   ```sh
   ng serve
   ```
   - App available at [http://localhost:4200](http://localhost:4200)

---

## API Endpoints

- **POST /upload**: Upload a document (PDF or text) for ingestion.
- **POST /query**: Submit a query and receive a retrieval-augmented response.
- **GET /health**: Health check endpoint.

See Swagger UI for detailed schemas.

---

## Sample Inputs

The `backend/sample_inputs/` directory contains:

- `meditations.pdf`: Example PDF for ingestion.
- `sample_query.txt`: Example query.
- `sample.json`: Example JSON input.
- `sample.txt`: Example plain text file.

---

## Advanced RAG Techniques

When submitting a query, users can select the retrieval strategy:

- **Basic**: Standard retrieval-augmented generation.
- **Hybrid Search**: Combines keyword and semantic search.
- **Reranking**: Retrieves candidates and reranks them using a secondary model.
- **Semantic Search**: Uses embeddings for retrieval.

The selected technique is sent to the backend as a `technique` parameter in the `/query` endpoint.

---

## Available Scripts

### Backend

- **Start server:** See above.
- **Install dependencies:** `pip install -r requirements.txt`

### Frontend

- **npm start / ng serve**: Start dev server.
- **npm run build / ng build**: Build for production.
- **npm test / ng test**: Run unit tests.
- **npm run lint / ng lint**: Lint codebase.
- **npm run e2e / ng e2e**: Run end-to-end tests.

---

## Implementation Overview

- **Backend:** FastAPI app with endpoints for document upload, query, and health check. Uses ChromaDB for vector storage and Ollama for LLM inference.
- **Frontend:** Angular app with components for upload, query, and results. Uses a dedicated service for API integration.
- **Component-Based UI:** Upload, query, and results display are organized as reusable Angular components.


---