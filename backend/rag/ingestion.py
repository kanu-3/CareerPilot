from pathlib import Path

from pypdf import PdfReader
from docx import Document as DocxDocument

from backend.database.connection import SessionLocal
from backend.database.model import Document
from backend.rag.chunking import split_text
from backend.rag.vectorstore import store_chunks


def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def extract_docx_text(file_path: str) -> str:
    document = DocxDocument(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    if extension == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    raise ValueError(
        f"Unsupported document type: {extension}"
    )


def ingest_document(
    file_path: str,
    user_id: int,
    document_type: str,
) -> int:

    path = Path(file_path)

    extracted_text = extract_text(file_path)

    if not extracted_text.strip():
        raise ValueError(
            "No text could be extracted from the document."
        )

    chunks = split_text(
    extracted_text,
    source_type=document_type,
)

    if not chunks:
        raise ValueError(
            "Document produced no usable chunks."
        )

    db = SessionLocal()

    try:
        document = Document(
            user_id=user_id,
            filename=path.name,
            document_type=document_type,
            file_path=str(path),
            extracted_text=extracted_text,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        document_id = document.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

    store_chunks(
        document_id=document_id,
        user_id=user_id,
        chunks=chunks,
    )

    return document_id