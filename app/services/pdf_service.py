from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)


class PDFService:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text(self) -> str:
        try:
            reader = PdfReader(self.pdf_path)
            pages = [p.extract_text() for p in reader.pages if p.extract_text()]
            return "\n".join(pages)
        except Exception as e:
            logger.exception("PDF extraction failed: %s", e)
            return ""