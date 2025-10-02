import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_file_path: str) -> str:
    """
    Extracts text from a PDF file using pypdf.

    Args:
        pdf_file_path (str): Path to the PDF file.

    Returns:
        str: Combined text from all pages.
    """
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"File not found: {pdf_file_path}")

    try:
        reader = PdfReader(pdf_file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error reading PDF: {e}")
