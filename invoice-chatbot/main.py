from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Invoice Summarization and Chatbot Assistant",
    description="A RAG-powered assistant for querying PDF invoices.",
    version="0.1.0"
)

# Health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Invoice Chatbot API is running."}

# Include API router
app.include_router(router, prefix="/api")

# To run the application, use the following command:
# uvicorn main:app --reload
