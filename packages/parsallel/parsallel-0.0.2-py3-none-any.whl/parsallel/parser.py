import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import pytesseract

class AutoParser:
    """
    AutoParser class for parsing PDFs in parallel using different methods.
    """

    def __init__(self, model="pypdf"):
        self.model = model

    def parse_pdf(self, pdf_path):
        if self.model.lower() == "pymupdf":
            return self._parse_with_pymupdf(pdf_path)
        elif self.model.lower() == "pypdf":
            return self._parse_with_pypdf(pdf_path)
        elif self.model.lower().startswith("ocr"):
            return self._parse_with_ocr(pdf_path)
        else:
            raise ValueError("Unsupported model specified.")

    def _parse_with_pymupdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        texts = []

        # Using ProcessPoolExecutor for multiprocessing
        with ProcessPoolExecutor() as executor:
            # Map the pages to the process pool and collect results
            results = executor.map(self._extract_text_pymupdf, range(len(doc))
            texts = list(results)

        doc.close()
        return "\n".join(texts)

    def _extract_text_pymupdf(self, page_number):
        # Re-open the document inside the process pool
        doc = fitz.open(pdf_path)
        page = doc[page_number]
        text = page.get_text()
        doc.close()
        return text

    def _parse_with_pypdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        texts = []

        # Using ProcessPoolExecutor for multiprocessing
        with ProcessPoolExecutor() as executor:
            # Map the pages to the process pool and collect results
            results = executor.map(self._extract_text_pypdf, range(len(reader.pages)))
            texts = list(results)

        return "\n".join(texts)

    def _extract_text_pypdf(self, page_number):
        # Re-open the document inside the process pool
        reader = PdfReader(pdf_path)
        page = reader.pages[page_number]
        text = page.extract_text()
        return text

    def _parse_with_ocr(self, pdf_path):
        doc = fitz.open(pdf_path)
        texts = []

        # Using ProcessPoolExecutor for multiprocessing
        with ProcessPoolExecutor() as executor:
            # Map the pages to the process pool and collect results
            results = executor.map(self._extract_text_ocr, range(len(doc))
            texts = list(results)

        doc.close()
        return "\n".join(texts)

    def _extract_text_ocr(self, page_number):
        # Re-open the document inside the process pool
        doc = fitz.open(pdf_path)
        page = doc[page_number]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        doc.close()
        return text
