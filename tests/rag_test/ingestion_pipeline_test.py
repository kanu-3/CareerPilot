from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User

from backend.rag.ingestion import ingest_document
from backend.rag.vectorstore import search_similar_chunks


FILE_PATH = r"C:\Users\Kanishka\Downloads\resume_aiml.pdf"


db = SessionLocal()

try:
    user = db.execute(
        select(User).where(
            User.email == "test@careerpilot.local"
        )
    ).scalar_one()

    user_id = user.id

finally:
    db.close()


document_id = ingest_document(
    file_path=FILE_PATH,
    user_id=user_id,
    document_type="resume",
)

print("Document ID:", document_id)


results = search_similar_chunks(
    query="What machine learning and AI projects has the candidate built?",
    user_id=user_id,
    limit=5,
)

print("\nRetrieved knowledge:")

for chunk, distance in results:
    print("\n---")
    print("Distance:", distance)
    print(chunk.content)