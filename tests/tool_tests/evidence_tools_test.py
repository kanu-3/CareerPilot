from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User
from backend.rag.retriever import retrieve_knowledge
from backend.tools.evidence_tool import find_skill_evidence


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


knowledge = retrieve_knowledge(
    query=(
        "What technical skills, tools, AI technologies, "
        "backend technologies, and projects does the "
        "candidate have?"
    ),
    user_id=user_id,
    limit=10,
)


skills_to_check = [
    "Python",
    "Machine Learning",
    "FastAPI",
    "LangChain",
    "PostgreSQL",
    "LangGraph",
    "RAG",
    "Docker",
]


for skill in skills_to_check:

    matches = find_skill_evidence(
        skill=skill,
        knowledge=knowledge,
    )

    print("\n==============================")
    print("SKILL:", skill)
    print("EVIDENCE FOUND:", bool(matches))

    for match in matches:
        print(
            f"Section: {match['section']} | "
            f"Project: {match['project']}"
        )