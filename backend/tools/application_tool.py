from datetime import datetime

from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Application, Job


VALID_STATUSES = {
    "considering",
    "applied",
    "interview",
    "rejected",
    "offer",
    "withdrawn",
}

VALID_INTERVIEW_STATUSES = {
    "not_started",
    "scheduled",
    "completed",
    "cancelled",
}


def create_application(
    user_id: int,
    job_id: int,
    resume_version: str | None = None,
    notes: str | None = None,
) -> dict:

    db = SessionLocal()

    try:
        # Verify job exists
        job = db.execute(
            select(Job).where(Job.id == job_id)
        ).scalar_one_or_none()

        if job is None:
            raise ValueError(
                f"Job {job_id} not found."
            )

        # Prevent duplicate active application
        existing = db.execute(
            select(Application).where(
                Application.user_id == user_id,
                Application.job_id == job_id,
                Application.status.not_in(
                    ["rejected", "withdrawn"]
                ),
            )
        ).scalar_one_or_none()

        if existing is not None:
            return {
                "success": False,
                "message": "An active application already exists for this job.",
                "application_id": existing.id,
                "job_id": existing.job_id,
                "status": existing.status,
            }

        application = Application(
            user_id=user_id,
            job_id=job_id,
            resume_version=resume_version,
            status="considering",
            interview_status="not_started",
            notes=notes,
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return {
            "success": True,
            "message": "Application created.",
            "application_id": application.id,
            "job_id": application.job_id,
            "status": application.status,
            "interview_status": application.interview_status,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_applications(
    user_id: int,
    status: str | None = None,
) -> list[dict]:

    if status is not None and status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Valid statuses: {sorted(VALID_STATUSES)}"
        )

    db = SessionLocal()

    try:
        statement = (
            select(Application, Job)
            .join(Job, Application.job_id == Job.id)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )

        if status is not None:
            statement = statement.where(
                Application.status == status
            )

        results = db.execute(statement).all()

        return [
            {
                "application_id": application.id,
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "job_url": job.job_url,
                "resume_version": application.resume_version,
                "status": application.status,
                "applied_at": application.applied_at,
                "interview_status": application.interview_status,
                "notes": application.notes,
                "outcome": application.outcome,
                "created_at": application.created_at,
            }
            for application, job in results
        ]

    finally:
        db.close()


def get_application(
    user_id: int,
    application_id: int,
) -> dict | None:

    db = SessionLocal()

    try:
        statement = (
            select(Application, Job)
            .join(Job, Application.job_id == Job.id)
            .where(
                Application.id == application_id,
                Application.user_id == user_id,
            )
        )

        result = db.execute(statement).first()

        if result is None:
            return None

        application, job = result

        return {
            "application_id": application.id,
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_url": job.job_url,
            "resume_version": application.resume_version,
            "status": application.status,
            "applied_at": application.applied_at,
            "interview_status": application.interview_status,
            "notes": application.notes,
            "outcome": application.outcome,
            "created_at": application.created_at,
        }

    finally:
        db.close()


def update_application(
    user_id: int,
    application_id: int,
    status: str | None = None,
    interview_status: str | None = None,
    notes: str | None = None,
    outcome: str | None = None,
) -> dict:

    if status is not None and status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Valid statuses: {sorted(VALID_STATUSES)}"
        )

    if (
        interview_status is not None
        and interview_status not in VALID_INTERVIEW_STATUSES
    ):
        raise ValueError(
            f"Invalid interview status "
            f"'{interview_status}'. "
            f"Valid statuses: "
            f"{sorted(VALID_INTERVIEW_STATUSES)}"
        )

    db = SessionLocal()

    try:
        application = db.execute(
            select(Application).where(
                Application.id == application_id,
                Application.user_id == user_id,
            )
        ).scalar_one_or_none()

        if application is None:
            raise ValueError(
                f"Application {application_id} not found."
            )

        if status is not None:
            application.status = status

            if status == "applied" and application.applied_at is None:
                application.applied_at = datetime.utcnow()

        if interview_status is not None:
            application.interview_status = interview_status

        if notes is not None:
            application.notes = notes

        if outcome is not None:
            application.outcome = outcome

        db.commit()
        db.refresh(application)

        return {
            "success": True,
            "application_id": application.id,
            "status": application.status,
            "applied_at": application.applied_at,
            "interview_status": application.interview_status,
            "notes": application.notes,
            "outcome": application.outcome,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()