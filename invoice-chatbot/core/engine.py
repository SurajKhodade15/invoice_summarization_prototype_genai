import os
from dotenv import load_dotenv
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
            raise ValueError("OPENAI_API_KEY not set in .env file.")

        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0
        )

        # Initialize Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize persistent Chroma vector store
        self.chroma_db_dir = "./chroma_db"
        os.makedirs(self.chroma_db_dir, exist_ok=True)
        self.vector_store = Chroma(
            persist_directory=self.chroma_db_dir,
            embedding_function=self.embeddings
        )

    def ingest_invoice(self, pdf_file_path: str):
        """
        Ingests a PDF invoice into the vector store.
        """
        text = extract_text_from_pdf(pdf_file_path)
        if not text:
            raise ValueError("No text extracted from PDF.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100
        )
        chunks = splitter.split_text(text)
        if not chunks:
            raise ValueError("No text chunks generated from PDF.")

        # Add chunks to vector store
        self.vector_store.add_texts(chunks)
        self.vector_store.persist()

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

        result = qa_chain({"query": query})
        return result
