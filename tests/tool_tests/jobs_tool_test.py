from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Job
from backend.tools.jobs_tool import get_job


db = SessionLocal()

try:
    job = db.execute(
        select(Job).where(
            Job.title == "AI Engineer"
        )
    ).scalars().first()

    if job is None:
        job = Job(
            title="AI Engineer",
            company="Test AI Company",
            location="Gurugram",
            job_url="https://example.com/jobs/ai-engineer",
            description=(
                "Build and deploy machine learning and "
                "AI applications."
            ),
            required_skills=(
                "Python, Machine Learning, FastAPI, "
                "LangChain, PostgreSQL"
            ),
            preferred_skills=(
                "LangGraph, RAG, Docker"
            ),
            experience_required="0-2 years",
            education_required="B.Tech or equivalent",
        )

        db.add(job)
        db.commit()
        db.refresh(job)

    job_id = job.id

finally:
    db.close()


result = get_job(job_id)

print("\n========== JOB ==========\n")
print(result)