import os
import logging
import langsmith
from dotenv import load_dotenv
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "invoice_app.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from utils.pdf_reader import extract_text_from_pdf

class InvoiceQASystem:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("OPENAI_API_KEY not set in .env file.")
            raise ValueError("OPENAI_API_KEY not set in .env file.")

        # Initialize LLM
        # LangSmith observability
        langsmith_project = "Invoice_Summarization"
        os.environ["LANGCHAIN_PROJECT"] = langsmith_project
        logger.info(f"LangSmith project set: {langsmith_project}")

        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0
        )
        logger.info("Initialized ChatOpenAI model.")

        # Initialize Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("Initialized HuggingFaceEmbeddings model.")

        # Initialize persistent Chroma vector store
        self.chroma_db_dir = "./chroma_db"
        os.makedirs(self.chroma_db_dir, exist_ok=True)
        self.vector_store = Chroma(
            persist_directory=self.chroma_db_dir,
            embedding_function=self.embeddings
        )
        logger.info("Initialized Chroma vector store.")

    def ingest_invoice(self, pdf_file_path: str):
        """
        Ingests a PDF invoice into the vector store.
        """
        logger.info(f"Ingesting invoice: {pdf_file_path}")
        text = extract_text_from_pdf(pdf_file_path)
        if not text:
            logger.error("No text extracted from PDF.")
            raise ValueError("No text extracted from PDF.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100
        )
        chunks = splitter.split_text(text)
        if not chunks:
            logger.error("No text chunks generated from PDF.")
            raise ValueError("No text chunks generated from PDF.")

        # Add chunks to vector store
        self.vector_store.add_texts(chunks)
        self.vector_store.persist()
        logger.info(f"Invoice ingested and persisted: {pdf_file_path}")

    def ask_question(self, query: str):
        """
        Answers a question using RAG over the ingested invoices.
        """
        prompt_template = """
You are a helpful assistant for finance professionals. Your task is to answer questions based ONLY on the provided context from an invoice.
If the answer is not found in the context, you must explicitly say "I cannot find the answer in the provided document." Do not make up information.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:
"""
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

        logger.info(f"Received query: {query}")
        result = qa_chain({"query": query})
        logger.info(f"Query result: {result}")
        return result
