import fitz  # PyMuPDF
from typing import BinaryIO

def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Extracts all text from a PDF file.

    Args:
        file (BinaryIO): A binary file-like object representing the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        # Use a context manager to ensure the PDF is properly closed
        with fitz.open(stream=file.read(), filetype="pdf") as pdf_doc:
            # Use a list to collect text for better performance
            text = [page.get_text() for page in pdf_doc]
        # Join the list into a single string and return
        return "".join(text)
    except Exception as e:
        # Handle errors (e.g., invalid PDF format)
        raise ValueError(f"Failed to extract text from PDF: {e}")
