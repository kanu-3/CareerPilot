from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User, Skill


def get_profile(user_id: int) -> dict | None:
    db = SessionLocal()

    try:
        user = db.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()

        if user is None:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "location": user.location,
            "target_roles": user.target_roles,
            "preferred_locations": user.preferred_locations,
            "salary_expectation": user.salary_expectation,
            "work_preference": user.work_preference,
            "education": user.education,
            "experience": user.experience,
            "career_goals": user.career_goals,
        }

    finally:
        db.close()

def get_skills(user_id: int) -> list[dict]:
    db = SessionLocal()

    try:
        skills = db.execute(
            select(Skill)
            .where(Skill.user_id == user_id)
            .order_by(Skill.name)
        ).scalars().all()

        return [
            {
                "id": skill.id,
                "name": skill.name,
                "proficiency": skill.proficiency,
                "evidence": skill.evidence,
                "source": skill.source,
                "verified": skill.verified,
                "last_updated": skill.last_updated,
            }
            for skill in skills
        ]

    finally:
        db.close()