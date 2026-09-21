"""PDF processing service module for text extraction and document parsing."""

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import fitz

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class PDFServiceError(Exception):
    """Base exception for PDF service errors."""


class InvalidPDFError(PDFServiceError):
    """Raised when the provided file is not a valid PDF."""


@dataclass(frozen=True)
class PDFPage:
    """Dataclass representing an extracted PDF page."""

    page_number: int
    text: str


@dataclass(frozen=True)
class PDFDocument:
    """Dataclass representing a structured PDF document with its extracted pages."""

    document_id: UUID
    document_name: str
    pages: list[PDFPage]


class PDFService:
    """Service responsible for extracting text from PDF documents."""

    def extract_document(
        self,
        file_path: Path,
        document_id: UUID,
    ) -> PDFDocument:
        """Extracts text content page-by-page from a target PDF file.

        Args:
            file_path: Path instance referencing the target PDF file.
            document_id: Unique UUID identifier for the document instance.

        Returns:
            PDFDocument: Structured representation containing extracted page texts.

        Raises:
            FileNotFoundError: If the target file path does not exist on disk.
            InvalidPDFError: If the extension is invalid or PyMuPDF fails to open it.
        """
        logger.info(
            "Starting PDF extraction: file=%s, document_id=%s",
            file_path,
            document_id,
        )

        if not file_path.exists():
            logger.error("PDF file not found: %s", file_path)
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            logger.error("Invalid PDF extension: %s", file_path)
            raise InvalidPDFError("The provided file must have a .pdf extension.")

        try:
            pdf_document = fitz.open(file_path)
        except Exception as exc:
            logger.exception("Unable to open PDF file: %s", file_path)
            raise InvalidPDFError(f"Unable to open PDF file: {file_path}") from exc

        try:
            pages = [
                PDFPage(
                    page_number=page_index + 1,
                    text=page.get_text(),
                )
                for page_index, page in enumerate(pdf_document)
            ]
        except Exception:
            logger.exception(
                "Failed to extract text from PDF: file=%s, document_id=%s",
                file_path,
                document_id,
            )
            raise
        finally:
            pdf_document.close()

        logger.info(
            "PDF extraction completed: file=%s, document_id=%s, pages=%d",
            file_path,
            document_id,
            len(pages),
        )

        return PDFDocument(
            document_id=document_id,
            document_name=file_path.name,
            pages=pages,
        )
