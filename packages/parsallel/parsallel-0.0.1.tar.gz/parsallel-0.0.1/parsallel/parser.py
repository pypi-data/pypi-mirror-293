import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor
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

        with ThreadPoolExecutor() as executor:
            results = executor.map(self._extract_text_pymupdf, doc)
            texts = list(results)

        doc.close()
        return "\n".join(texts)

    def _extract_text_pymupdf(self, page):
        return page.get_text()

    def _parse_with_pypdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        texts = []

        with ThreadPoolExecutor() as executor:
            results = executor.map(self._extract_text_pypdf, reader.pages)
            texts = list(results)

        return "\n".join(texts)

    def _extract_text_pypdf(self, page):
        return page.extract_text()

    def _parse_with_ocr(self, pdf_path):
        doc = fitz.open(pdf_path)
        texts = []

        with ThreadPoolExecutor() as executor:
            results = executor.map(self._extract_text_ocr, doc)
            texts = list(results)

        doc.close()
        return "\n".join(texts)

    def _extract_text_ocr(self, page):
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return pytesseract.image_to_string(img)