from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User
from backend.rag.ragans import answer_from_knowledge


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


result = answer_from_knowledge(
    query="What AI and machine learning projects has the candidate built?",
    user_id=user_id,
)


print("\n========== ANSWER ==========\n")
print(result["answer"])

print("\n========== SOURCES ==========\n")

for source in result["sources"]:
    print("--------------------")
    print("Document:", source["document_id"])
    print("Section:", source["section"])
    print("Project:", source["project"])
    print("Source:", source["source_type"])