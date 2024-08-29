import os
import requests
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

def load_pdf(source):
    """
    Load PDF files from a file, directory, or URL.
    """
    pdfs = []

    if os.path.isfile(source):
        pdfs.append(source)
    elif os.path.isdir(source):
        for file_name in os.listdir(source):
            if file_name.endswith('.pdf'):
                pdfs.append(os.path.join(source, file_name))
    elif source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        file_name = "temp_pdf_from_url.pdf"
        with open(file_name, "wb") as f:
            f.write(response.content)
        pdfs.append(file_name)
    else:
        raise ValueError("Invalid source type. Must be a file, directory, or URL.")

    return pdfs