from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User
from backend.rag.retriever import retrieve_knowledge


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


results = retrieve_knowledge(
    query="What AI and machine learning projects has the candidate built?",
    user_id=user_id,
    limit=5,
)


print("Retrieved knowledge:")

for result in results:
    print("\n--------------------")
    print("Chunk ID:", result["chunk_id"])
    print("Document ID:", result["document_id"])
    print("Section:", result["section"])
    print("Project:", result["project"])
    print("Source:", result["source_type"])
    print("Distance:", result["distance"])
    print("Content:")
    print(result["content"])