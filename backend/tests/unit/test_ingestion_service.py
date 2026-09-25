"""Unit tests for the document ingestion and text chunking service."""

from uuid import uuid4

import pytest

from backend.app.services.ingestion_service import IngestionService
from backend.app.services.pdf_service import PDFDocument, PDFPage


@pytest.fixture
def ingestion_service() -> IngestionService:
    """Provides a fresh IngestionService instance for testing."""
    return IngestionService()


@pytest.fixture
def document() -> PDFDocument:
    """Provides a sample PDFDocument populated with test text."""
    return PDFDocument(
        document_id=uuid4(),
        document_name="example.pdf",
        pages=[
            PDFPage(
                page_number=1,
                text="A" * 1000,
            )
        ],
    )


def test_chunk_document_preserves_page_metadata(
    ingestion_service: IngestionService,
    document: PDFDocument,
) -> None:
    """Tests that generated chunks retain parent document and page metadata."""
    chunks = ingestion_service.chunk_document(
        document,
        chunk_size=500,
        chunk_overlap=100,
    )

    assert chunks
    assert all(chunk.document_id == document.document_id for chunk in chunks)
    assert all(chunk.document_name == document.document_name for chunk in chunks)
    assert all(chunk.page_number == 1 for chunk in chunks)


def test_chunk_document_respects_chunk_size(
    ingestion_service: IngestionService,
    document: PDFDocument,
) -> None:
    """Tests that generated chunks do not exceed maximum specified size."""
    chunks = ingestion_service.chunk_document(
        document,
        chunk_size=200,
        chunk_overlap=50,
    )

    assert chunks
    assert all(len(chunk.text) <= 200 for chunk in chunks)


def test_chunk_document_applies_overlap(
    ingestion_service: IngestionService,
    document: PDFDocument,
) -> None:
    """Tests that consecutive chunks maintain the configured character overlap."""
    chunks = ingestion_service.chunk_document(
        document,
        chunk_size=200,
        chunk_overlap=50,
    )

    assert len(chunks) > 1
    assert chunks[0].text[-50:] == chunks[1].text[:50]


def test_chunk_document_skips_empty_pages(
    ingestion_service: IngestionService,
) -> None:
    """Tests that document pages with empty text are ignored during chunking."""
    document = PDFDocument(
        document_id=uuid4(),
        document_name="example.pdf",
        pages=[
            PDFPage(page_number=1, text=""),
            PDFPage(page_number=2, text="content"),
        ],
    )

    chunks = ingestion_service.chunk_document(
        document,
        chunk_size=500,
        chunk_overlap=100,
    )

    assert len(chunks) == 1
    assert chunks[0].page_number == 2


@pytest.mark.parametrize(
    ("chunk_size", "chunk_overlap"),
    [
        (0, 100),
        (-1, 100),
        (100, -1),
        (100, 100),
        (100, 150),
    ],
)
def test_chunk_document_rejects_invalid_chunk_configuration(
    ingestion_service: IngestionService,
    document: PDFDocument,
    chunk_size: int,
    chunk_overlap: int,
) -> None:
    """Tests that ValueError is raised for invalid chunk configuration settings."""
    with pytest.raises(ValueError):
        ingestion_service.chunk_document(
            document,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
