import os
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from models.schemas import QueryRequest, QueryResponse, UploadResponse
from core.engine import InvoiceQASystem

router = APIRouter()
UPLOAD_DIR = "./temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Singleton instance of the QA system
qa_system = InvoiceQASystem()

@router.post("/upload_invoice/", response_model=UploadResponse)
async def upload_invoice(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        qa_system.ingest_invoice(file_path)
        return UploadResponse(
            filename=file.filename,
            message="Invoice uploaded and ingested successfully."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process invoice: {e}"
        )

@router.post("/query/", response_model=QueryResponse)
async def query_invoice(request: QueryRequest):
    try:
        result = qa_system.ask_question(request.query)
        answer = result.get("result", "")
        source_docs = result.get("source_documents", [])
        return QueryResponse(
            query=request.query,
            answer=answer,
            source_documents=source_docs
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer query: {e}"
        )
