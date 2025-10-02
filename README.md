# Invoice Summarization & Chatbot Assistant

A Retrieval-Augmented Generation (RAG) application for finance professionals to upload PDF invoices and ask questions about their content using natural language. The system leverages FastAPI, LangChain, OpenAI, Hugging Face embeddings, ChromaDB, and Streamlit for a complete end-to-end solution.

---

## Features
- **Invoice Upload:** Upload PDF invoices for instant processing.
- **RAG-powered Q&A:** Ask questions about invoice content and get accurate, context-based answers.
- **Source Document Traceability:** See which invoice snippets were used to answer your question.
- **Modern UI:** Responsive Streamlit frontend for easy interaction.

---


## Technology Stack & Rationale

1. **FastAPI (Backend API):**
	- Chosen for its speed, async support, and automatic OpenAPI docs.
	- Handles invoice upload and Q&A endpoints.

2. **Streamlit (Frontend):**
	- Enables rapid development of interactive web apps in Python.
	- Provides a user-friendly UI for uploading invoices and asking questions.

3. **LangChain (AI Orchestration):**
	- Manages LLM chains, document retrieval, and prompt engineering.
	- Integrates with vector DBs and supports RAG workflows.

4. **OpenAI GPT-3.5-turbo (LLM):**
	- Delivers high-quality, context-aware answers.
	- Used for answering questions based on invoice content.

5. **Hugging Face Sentence Transformers (Embeddings):**
	- `sentence-transformers/all-MiniLM-L6-v2` for efficient, high-quality text embeddings.
	- Converts invoice text into vectors for semantic search.

6. **ChromaDB (Vector Database):**
	- Stores and retrieves text chunks using embeddings.
	- Enables fast, persistent similarity search for RAG.

7. **PyPDF (PDF Parsing):**
	- Extracts text from uploaded PDF invoices.
	- Handles multi-page and complex invoice layouts.

8. **python-dotenv (Configuration):**
	- Loads environment variables securely (API keys, config).

9. **Pydantic (Validation):**
	- Ensures robust data validation for API requests and responses.

10. **LangSmith (Observability):**
	 - Tracks and visualizes LLM chain executions for debugging and monitoring.

11. **Logging (Python logging):**
	 - Captures all key events and errors for audit and troubleshooting.

12. **Custom Metrics (Precision@k, Recall@k):**
	 - Measures retrieval accuracy for continuous improvement.

---

---

## Project Structure
```
invoice-chatbot/
├── .env
├── requirements.txt
├── main.py
├── app.py                # Streamlit frontend
├── api/
│   └── routes.py
├── core/
│   └── engine.py
├── models/
│   └── schemas.py
├── utils/
│   └── pdf_reader.py
├── chroma_db/
├── temp_uploads/
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd invoice-chatbot
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set OpenAI API Key
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Run FastAPI Backend
```bash
uvicorn main:app --reload
```

### 6. Run Streamlit Frontend
```bash
streamlit run app.py
```

---

## Usage Demo
1. **Upload Invoice:** Use the Streamlit UI to upload a PDF invoice.
2. **Ask Questions:** Enter your question about the invoice and get an answer with supporting document snippets.
3. **Traceability:** Expand source documents to see the context used for the answer.

---

## API Endpoints
- `POST /api/upload_invoice/` — Upload a PDF invoice.
- `POST /api/query/` — Ask a question about the uploaded invoice.

---

## Screenshots
> ![Streamlit UI Screenshot](demo_screenshot.png)

---


## Why This Stack?

- **FastAPI**: Modern, async, and easy to integrate with Python ML stack.
- **Streamlit**: Fastest way to build interactive Python apps for demos and prototyping.
- **LangChain**: Industry standard for RAG, LLM chaining, and retrieval workflows.
- **OpenAI GPT-3.5-turbo**: Reliable, high-quality LLM for finance and document Q&A.
- **Hugging Face Embeddings**: State-of-the-art semantic search for document chunks.
- **ChromaDB**: Open-source, persistent, and fast for vector search.
- **LangSmith**: Observability and debugging for LLM chains.
- **Logging & Metrics**: Ensures reliability, traceability, and measurable accuracy.

## Additional Information

- **Extensible:** Easily add support for other document types, LLMs, or vector DBs.
- **Security:** API keys and sensitive config are loaded via `.env` and never hardcoded.
- **Demo Ready:** All code runs locally; no cloud dependencies required for demo.
- **Monitoring:** LangSmith and logging provide full traceability for every request.
- **Accuracy:** Precision@k and Recall@k metrics can be used to benchmark and improve retrieval.

## For Interviewers / Reviewers
- **End-to-End Demo:** Both backend and frontend run locally.
- **Tech Stack:** Modern Python, FastAPI, LangChain, OpenAI, ChromaDB, Streamlit, LangSmith.
- **Extensible:** Easily adaptable for other document types, LLMs, or enterprise use.

---

## License
MIT
