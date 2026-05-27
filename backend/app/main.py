from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.query_engine import execute_multimodal_query
from app.pipeline import run_multimodal_ingestion_pipeline
from app.vector_store import index_multimodal_payload

app = FastAPI(title="Multi-Modal PDF RAG API")

class QueryRequest(BaseModel):
    question: str

class IngestRequest(BaseModel):
    pdf_path: str

@app.post("/ingest")
async def ingest_file(payload: IngestRequest):
    try:
        processed_data = run_multimodal_ingestion_pipeline(payload.pdf_path)
        index_multimodal_payload(processed_data)
        return {"status": "success", "message": f"Successfully indexed {payload.pdf_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(req: QueryRequest):

    try:

        result = execute_multimodal_query(
            req.question
        )

        return result

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)