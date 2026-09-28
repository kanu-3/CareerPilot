from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User, Document

from backend.rag.chunking import split_text
from backend.rag.vectorstore import (
    store_chunks,
    search_similar_chunks,
)

db = SessionLocal()

try:
    user = db.execute(
        select(User).where(
            User.email == "test@careerpilot.local"
        )
    ).scalar_one_or_none()

    if user is None:
        user = User(
            name="Test User",
            email="test@careerpilot.local",
            location="Delhi NCR",
            target_roles="AI Engineer, ML Engineer",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    user_id = user.id

    document = Document(
        user_id=user_id,
        filename="test_resume.txt",
        document_type="resume",
        file_path="data/test_resume.txt",
        extracted_text="""
        The candidate has experience with Python,
        FastAPI, machine learning, LangChain,
        LangGraph, PostgreSQL, Supabase, and
        generative AI applications.
        """,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    document_id = document.id
    document_text = document.extracted_text

finally:
    db.close()

text = document_text

chunks = split_text(text)

print("Chunks created:", len(chunks))

stored = store_chunks(
    document_id=document_id,
    user_id=user_id,
    chunks=chunks,
)

print("Chunks stored:", stored)

results = search_similar_chunks(
    query="What backend technologies does the candidate know?",
    user_id=user_id,
    limit=3,
)

print("\nSearch results:")

for chunk, distance in results:
    print("\n---")
    print("Distance:", distance)
    print("Content:", chunk.content)