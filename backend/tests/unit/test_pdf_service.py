"""Unit tests for PDF document text extraction service and error handling."""

from pathlib import Path
from uuid import uuid4

import fitz
import pytest

from backend.app.services.pdf_service import (
    InvalidPDFError,
    PDFService,
)


@pytest.fixture
def pdf_service() -> PDFService:
    """Provides a fresh PDFService instance for test execution."""
    return PDFService()


def create_pdf(file_path: Path, pages: list[str]) -> None:
    """Helper utility to generate temporary real PDF files for testing.

    Args:
        file_path: Target output path for the PDF file.
        pages: List of string contents to populate individual pages.
    """
    document = fitz.open()

    for text in pages:
        page = document.new_page()
        page.insert_text((72, 72), text)

    document.save(file_path)
    document.close()


def test_extract_document_returns_page_text(
    pdf_service: PDFService,
    tmp_path: Path,
) -> None:
    """Tests that text content is correctly extracted from a single-page PDF."""
    pdf_path = tmp_path / "example.pdf"
    create_pdf(pdf_path, ["First page content"])

    document_id = uuid4()

    result = pdf_service.extract_document(pdf_path, document_id)

    assert result.document_id == document_id
    assert result.document_name == "example.pdf"
    assert len(result.pages) == 1
    assert "First page content" in result.pages[0].text


def test_extract_document_preserves_page_numbers(
    pdf_service: PDFService,
    tmp_path: Path,
) -> None:
    """Tests that multi-page PDFs retain sequential page numbers and content."""
    pdf_path = tmp_path / "multi-page.pdf"
    create_pdf(
        pdf_path,
        [
            "Content from page one",
            "Content from page two",
            "Content from page three",
        ],
    )

    result = pdf_service.extract_document(pdf_path, uuid4())

    assert len(result.pages) == 3
    assert [page.page_number for page in result.pages] == [1, 2, 3]
    assert "Content from page one" in result.pages[0].text
    assert "Content from page two" in result.pages[1].text
    assert "Content from page three" in result.pages[2].text


def test_extract_document_raises_for_missing_file(
    pdf_service: PDFService,
    tmp_path: Path,
) -> None:
    """Tests that a FileNotFoundError is raised when file does not exist."""
    pdf_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        pdf_service.extract_document(pdf_path, uuid4())


def test_extract_document_raises_for_invalid_extension(
    pdf_service: PDFService,
    tmp_path: Path,
) -> None:
    """Tests that an InvalidPDFError is raised when file extension is not .pdf."""
    file_path = tmp_path / "document.txt"
    file_path.write_text("This is not a PDF.")

    with pytest.raises(InvalidPDFError):
        pdf_service.extract_document(file_path, uuid4())


def test_extract_document_raises_for_corrupted_pdf(
    pdf_service: PDFService,
    tmp_path: Path,
) -> None:
    """Tests that an InvalidPDFError is raised when reading a corrupted file."""
    pdf_path = tmp_path / "corrupted.pdf"
    pdf_path.write_bytes(b"This is a corrupted PDF file.")

    with pytest.raises(InvalidPDFError):
        pdf_service.extract_document(pdf_path, uuid4())


def test_extract_document_supports_empty_pdf(
    pdf_service: PDFService,
    tmp_path: Path,
) -> None:
    """Tests that processing a PDF with a blank page returns empty text."""
    pdf_path = tmp_path / "empty.pdf"

    document = fitz.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    result = pdf_service.extract_document(pdf_path, uuid4())

    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1
    assert result.pages[0].text == ""

