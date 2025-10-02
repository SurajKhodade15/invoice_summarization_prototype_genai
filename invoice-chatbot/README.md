# Invoice Summarization & Chatbot Assistant

A Retrieval-Augmented Generation (RAG) application for finance professionals to upload PDF invoices and ask questions about their content using natural language. The system leverages FastAPI, LangChain, OpenAI, Hugging Face embeddings, ChromaDB, and Streamlit for a complete end-to-end solution.

---

## Features
- **Invoice Upload:** Upload PDF invoices for instant processing.
- **RAG-powered Q&A:** Ask questions about invoice content and get accurate, context-based answers.
- **Source Document Traceability:** See which invoice snippets were used to answer your question.
- **Modern UI:** Responsive Streamlit frontend for easy interaction.

---

## Technology Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **AI Orchestration:** LangChain
- **LLM:** OpenAI GPT-3.5-turbo
- **Embeddings:** Hugging Face `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB:** ChromaDB (persistent)
- **PDF Parsing:** PyPDF
- **Config:** python-dotenv
- **Validation:** Pydantic

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

## For Interviewers / Reviewers
- **End-to-End Demo:** Both backend and frontend run locally.
- **Tech Stack:** Modern Python, FastAPI, LangChain, OpenAI, ChromaDB, Streamlit.
- **Extensible:** Easily adaptable for other document types or LLMs.

---

## License
MIT
