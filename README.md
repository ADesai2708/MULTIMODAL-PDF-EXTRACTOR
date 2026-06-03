# Multimodal PDF RAG System

A Retrieval-Augmented Generation (RAG) system that enables users to upload PDF documents, extract both textual and visual information, and ask natural language questions about the content.

The project combines document parsing, image understanding, vector search, and LLM-powered question answering to provide context-aware responses from technical documents, research papers, reports, and similar PDFs.

---

## Features

* PDF document ingestion and processing
* Text extraction from PDF files
* Image extraction using PyMuPDF
* Image caption generation using BLIP
* Semantic search using vector embeddings
* Qdrant vector database integration
* Context-aware question answering
* FastAPI-based REST endpoints
* Support for multimodal retrieval (text + visual content)

---

## Tech Stack

### Backend

* Python
* FastAPI

### AI / ML

* Sentence Transformers
* BLIP Image Captioning
* Transformers
* Hugging Face Models

### Vector Database

* Qdrant

### Document Processing

* PyMuPDF (fitz)
* LlamaParse

---

## Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   ├── parser.py
│   ├── pipeline.py
│   ├── query_engine.py
│   ├── vector_store.py
│   ├── vision_analyzer.py
│   └── config.py
│
├── data/
│   ├── input_pdfs/
│   ├── extracted_images/
│   └── qdrant_db/
│
└── requirements.txt
```

---

## Workflow

1. Upload a PDF document.
2. Extract textual content and embedded images.
3. Generate captions for extracted images using BLIP.
4. Convert text and image descriptions into embeddings.
5. Store embeddings in Qdrant.
6. Retrieve relevant context based on user queries.
7. Generate answers using retrieved information.

---

## API Endpoints

### Ingest Document

```http
POST /ingest
```

Indexes a PDF document into the vector database.

### Query Document

```http
POST /query
```

Returns answers based on the indexed document content.

---

## Running Locally

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start API Server

```bash
uvicorn app.main:app --reload
```

### Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## Challenges Faced

* Handling PDF documents containing both text and images.
* Managing dependency conflicts between AI libraries.
* Generating useful descriptions for extracted visual elements.
* Designing a retrieval pipeline that combines textual and visual context.

---

## Future Improvements

* Support for DOCX and PPTX files.
* Hybrid search (keyword + vector search).
* OCR support for scanned PDFs.
* Chat history and conversational memory.
* AWS deployment with managed vector storage.

---

## Author

Anjali Desai

Built as a learning project to explore Retrieval-Augmented Generation (RAG), vector databases, document intelligence, and multimodal AI systems.
