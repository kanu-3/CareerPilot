from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import DocumentChunk
from backend.llm.embeddings import embedding_model
from backend.rag.chunking import Chunk


def store_chunks(
    document_id: int,
    user_id: int,
    chunks: list[Chunk],
) -> int:
    db = SessionLocal()

    try:
        for chunk in chunks:
            embedding = embedding_model.embed_text(
                chunk.content
            )

            document_chunk = DocumentChunk(
                document_id=document_id,
                user_id=user_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                section=chunk.section,
                project=chunk.project,
                source_type=chunk.source_type,
                embedding=embedding,
            )

            db.add(document_chunk)

        db.commit()

        return len(chunks)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def search_similar_chunks(
    query: str,
    user_id: int,
    limit: int = 5,
):
    query_embedding = embedding_model.embed_text(query)

    db = SessionLocal()

    try:
        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        statement = (
            select(DocumentChunk, distance.label("distance"))
            .where(DocumentChunk.user_id == user_id)
            .order_by(distance)
            .limit(limit)
        )

        return db.execute(statement).all()

    finally:
        db.close()