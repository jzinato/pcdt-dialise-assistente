import fitz  # PyMuPDF

def extract_text_from_pdf(file) -> str:
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text