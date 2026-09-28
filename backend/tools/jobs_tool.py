from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Job


def get_job(job_id: int) -> dict | None:
    db = SessionLocal()

    try:
        job = db.execute(
            select(Job).where(Job.id == job_id)
        ).scalar_one_or_none()

        if job is None:
            return None

        return {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_url": job.job_url,
            "description": job.description,
            "required_skills": job.required_skills,
            "preferred_skills": job.preferred_skills,
            "experience_required": job.experience_required,
            "education_required": job.education_required,
            "status": job.status,
            "match_score": job.match_score,
        }

    finally:
        db.close()