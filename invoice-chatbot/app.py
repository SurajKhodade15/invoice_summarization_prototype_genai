import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Invoice Summarization & Chatbot Assistant", layout="wide")
st.sidebar.title("Invoice Summarization & Chatbot Assistant")
st.sidebar.markdown("""
Upload your PDF invoice and ask questions about its content. Powered by FastAPI, LangChain, OpenAI, and ChromaDB.
""")

st.title("Invoice Summarization & Chatbot Assistant")

# --- Invoice Upload ---
st.header("1. Upload Invoice PDF")
uploaded_file = st.file_uploader("Choose a PDF invoice", type=["pdf"])
if uploaded_file:
    if st.button("Upload Invoice"):
        with st.spinner("Uploading and processing invoice..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            try:
                response = requests.post(f"{API_URL}/upload_invoice/", files=files)
                if response.status_code == 200:
                    st.success(f"Uploaded: {uploaded_file.name}")
                else:
                    st.error(f"Upload failed: {response.json().get('detail', response.text)}")
            except Exception as e:
                st.error(f"Error: {e}")

st.header("2. Ask a Question About the Invoice")
query = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying the invoice..."):
            try:
                payload = {"query": query}
                response = requests.post(f"{API_URL}/query/", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Answer:")
                    st.write(data["answer"])
                    st.subheader("Source Documents:")
                    for i, doc in enumerate(data["source_documents"]):
                        with st.expander(f"Source Document {i+1}"):
                            st.write(doc)
                else:
                    st.error(f"Query failed: {response.json().get('detail', response.text)}")
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Demo: Upload an invoice and ask questions. All processing is local.")
