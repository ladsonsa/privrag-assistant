"""Document ingestion service for text chunking."""

from dataclasses import dataclass
from uuid import UUID

from backend.app.services.pdf_service import PDFDocument


@dataclass(frozen=True)
class DocumentChunk:
    """Represents a chunk of text extracted from a document page."""

    chunk_id: str
    text: str
    document_id: UUID
    document_name: str
    page_number: int


class IngestionService:
    """Service responsible for preparing document text for ingestion."""

    def chunk_document(
        self,
        document: PDFDocument,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
    ) -> list[DocumentChunk]:
        """Splits document pages into overlapping text chunks.

        Args:
            document: Structured PDF document with page-level text.
            chunk_size: Maximum number of characters per chunk.
            chunk_overlap: Number of characters shared between consecutive
                chunks.

        Returns:
            list[DocumentChunk]: List of document chunks preserving page origin.

        Raises:
            ValueError: If chunk_size or chunk_overlap parameters are invalid.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")

        chunks: list[DocumentChunk] = []

        chunk_index = 0

        for page in document.pages:
            text = page.text

            if not text:
                continue

            start = 0

            while start < len(text):
                end = start + chunk_size
                chunk_text = text[start:end]

                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{document.document_id}-{chunk_index}",
                        text=chunk_text,
                        document_id=document.document_id,
                        document_name=document.document_name,
                        page_number=page.page_number,
                    )
                )

                chunk_index += 1

                if end >= len(text):
                    break

                start = end - chunk_overlap

        return chunks
