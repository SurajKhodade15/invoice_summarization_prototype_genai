import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from models.schemas import QueryRequest, QueryResponse, UploadResponse
from core.engine import InvoiceQASystem

router = APIRouter()
UPLOAD_DIR = "./temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "api.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

# Singleton instance of the QA system
qa_system = InvoiceQASystem()

@router.post("/upload_invoice/", response_model=UploadResponse)
async def upload_invoice(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"File uploaded: {file.filename}")
        qa_system.ingest_invoice(file_path)
        logger.info(f"Invoice ingested: {file.filename}")
        return UploadResponse(
            filename=file.filename,
            message="Invoice uploaded and ingested successfully."
        )
    except Exception as e:
        logger.error(f"Failed to process invoice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process invoice: {e}"
        )

@router.post("/query/", response_model=QueryResponse)
async def query_invoice(request: QueryRequest):
    try:
        logger.info(f"Received query: {request.query}")
        result = qa_system.ask_question(request.query)
        answer = result.get("result", "")
        source_docs = result.get("source_documents", [])
        logger.info(f"Query answered: {answer}")
        return QueryResponse(
            query=request.query,
            answer=answer,
            source_documents=source_docs
        )
    except Exception as e:
        logger.error(f"Failed to answer query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer query: {e}"
        )
