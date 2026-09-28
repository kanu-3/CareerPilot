from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Job, SavedJob


VALID_STATUSES = {
    "saved",
    "considering",
    "applied",
    "archived",
}


def save_job(
    user_id: int,
    job_id: int,
    notes: str | None = None,
) -> dict:

    db = SessionLocal()

    try:
        job = db.execute(
            select(Job).where(Job.id == job_id)
        ).scalar_one_or_none()

        if job is None:
            raise ValueError(
                f"Job {job_id} not found."
            )

        # Check whether already saved
        existing = db.execute(
            select(SavedJob).where(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id,
            )
        ).scalar_one_or_none()

        if existing is not None:
            return {
                "success": False,
                "message": "Job is already saved.",
                "saved_job_id": existing.id,
                "job_id": existing.job_id,
                "status": existing.status,
            }

        saved_job = SavedJob(
            user_id=user_id,
            job_id=job_id,
            status="saved",
            notes=notes,
        )

        db.add(saved_job)
        db.commit()
        db.refresh(saved_job)

        return {
            "success": True,
            "message": "Job saved successfully.",
            "saved_job_id": saved_job.id,
            "job_id": saved_job.job_id,
            "status": saved_job.status,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_saved_jobs(user_id: int) -> list[dict]:

    db = SessionLocal()

    try:
        statement = (
            select(SavedJob, Job)
            .join(Job, SavedJob.job_id == Job.id)
            .where(SavedJob.user_id == user_id)
            .order_by(SavedJob.created_at.desc())
        )

        results = db.execute(statement).all()

        saved_jobs = []

        for saved_job, job in results:

            saved_jobs.append(
                {
                    "saved_job_id": saved_job.id,
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "job_url": job.job_url,
                    "status": saved_job.status,
                    "notes": saved_job.notes,
                    "saved_at": saved_job.created_at,
                }
            )

        return saved_jobs

    finally:
        db.close()


def get_saved_job(
    user_id: int,
    job_id: int,
) -> dict | None:

    db = SessionLocal()

    try:
        statement = (
            select(SavedJob, Job)
            .join(Job, SavedJob.job_id == Job.id)
            .where(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id,
            )
        )

        result = db.execute(statement).first()

        if result is None:
            return None

        saved_job, job = result

        return {
            "saved_job_id": saved_job.id,
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_url": job.job_url,
            "status": saved_job.status,
            "notes": saved_job.notes,
            "saved_at": saved_job.created_at,
        }

    finally:
        db.close()


def update_job_status(
    user_id: int,
    job_id: int,
    status: str,
) -> dict:

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Valid statuses: {sorted(VALID_STATUSES)}"
        )

    db = SessionLocal()

    try:
        saved_job = db.execute(
            select(SavedJob).where(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id,
            )
        ).scalar_one_or_none()

        if saved_job is None:
            raise ValueError(
                f"Job {job_id} is not saved by user {user_id}."
            )

        saved_job.status = status

        db.commit()
        db.refresh(saved_job)

        return {
            "success": True,
            "saved_job_id": saved_job.id,
            "job_id": saved_job.job_id,
            "status": saved_job.status,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def remove_saved_job(
    user_id: int,
    job_id: int,
) -> dict:

    db = SessionLocal()

    try:
        saved_job = db.execute(
            select(SavedJob).where(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id,
            )
        ).scalar_one_or_none()

        if saved_job is None:
            return {
                "success": False,
                "message": "Saved job not found.",
            }

        db.delete(saved_job)
        db.commit()

        return {
            "success": True,
            "message": "Job removed from saved jobs.",
            "job_id": job_id,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()