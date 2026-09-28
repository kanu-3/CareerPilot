import json
from pathlib import Path

from backend.database.connection import SessionLocal
from backend.database.model import Job


SEED_FILE = Path("data/seed/jobs.json")


def seed_jobs():
    with open(SEED_FILE, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    db = SessionLocal()

    try:
        existing_jobs = db.query(Job).all()

        existing_keys = {
            (
                job.title.strip().lower(),
                job.company.strip().lower(),
            )
            for job in existing_jobs
        }

        added = 0
        skipped = 0

        for job_data in jobs:

            key = (
                job_data["title"].strip().lower(),
                job_data["company"].strip().lower(),
            )

            if key in existing_keys:
                skipped += 1
                continue

            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                job_url=job_data["job_url"],
                description=job_data["description"],
                required_skills=job_data["required_skills"],
                preferred_skills=job_data["preferred_skills"],
                experience_required=job_data["experience_required"],
                education_required=job_data["education_required"],
                status=job_data["status"],
            )

            db.add(job)
            existing_keys.add(key)
            added += 1

        db.commit()

        print(f"Added: {added}")
        print(f"Skipped existing: {skipped}")
        print(f"Total jobs now: {db.query(Job).count()}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_jobs()