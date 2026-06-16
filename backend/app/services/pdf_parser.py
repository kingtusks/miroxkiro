from PyPDF2 import PdfReader
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text content from a PDF file."""
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)
