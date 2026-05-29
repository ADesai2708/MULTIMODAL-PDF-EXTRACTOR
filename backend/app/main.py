from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from app.query_engine import execute_multimodal_query
from app.pipeline import run_multimodal_ingestion_pipeline
from app.vector_store import index_multimodal_payload

app = FastAPI(title="Multi-Modal PDF RAG API")

# 1. Enable CORS for React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Expose the extracted images directory publicly via HTTP
IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/extracted_images"))
os.makedirs(IMAGE_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

class QueryRequest(BaseModel):
    question: str

class IngestRequest(BaseModel):
    pdf_path: str

@app.post("/ingest")
async def ingest_file(payload: IngestRequest):
    try:
        processed_data = run_multimodal_ingestion_pipeline(payload.pdf_path)
        index_multimodal_payload(processed_data)
        return {"status": "success", "message": "Successfully indexed document structure."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_rag(payload: QueryRequest):
    try:
        response_data = execute_multimodal_query(payload.question)

        web_referenced_images = []
        for img in response_data.get("referenced_images", []):
            filename = os.path.basename(img["path"])
            web_referenced_images.append({
                "name": img.get("name") or filename,
                "url": f"http://localhost:8000/images/{filename}"
            })

        return {
            "answer": response_data["answer"],
            "referenced_images": web_referenced_images
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)