from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import LearningTask


VALID_PRIORITIES = {
    "low",
    "medium",
    "high",
}

VALID_STATUSES = {
    "pending",
    "in_progress",
    "completed",
}


def create_learning_task(
    user_id: int,
    skill: str,
    title: str,
    description: str,
    priority: str = "medium",
    resource_url: str | None = None,
    due_date=None,
) -> dict:

    if priority not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{priority}'. "
            f"Valid priorities: {sorted(VALID_PRIORITIES)}"
        )

    db = SessionLocal()

    try:
        task = LearningTask(
            user_id=user_id,
            skill=skill,
            title=title,
            description=description,
            priority=priority,
            status="pending",
            resource_url=resource_url,
            due_date=due_date,
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "skill": task.skill,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "resource_url": task.resource_url,
            "due_date": task.due_date,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_learning_tasks(
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
            select(LearningTask)
            .where(LearningTask.user_id == user_id)
            .order_by(LearningTask.created_at.desc())
        )

        if status is not None:
            statement = statement.where(
                LearningTask.status == status
            )

        tasks = db.execute(statement).scalars().all()

        return [
            {
                "task_id": task.id,
                "skill": task.skill,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "resource_url": task.resource_url,
                "due_date": task.due_date,
                "created_at": task.created_at,
            }
            for task in tasks
        ]

    finally:
        db.close()


def update_learning_task(
    user_id: int,
    task_id: int,
    status: str | None = None,
    priority: str | None = None,
) -> dict:

    if status is not None and status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Valid statuses: {sorted(VALID_STATUSES)}"
        )

    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{priority}'. "
            f"Valid priorities: {sorted(VALID_PRIORITIES)}"
        )

    db = SessionLocal()

    try:
        task = db.execute(
            select(LearningTask).where(
                LearningTask.id == task_id,
                LearningTask.user_id == user_id,
            )
        ).scalar_one_or_none()

        if task is None:
            raise ValueError(
                f"Learning task {task_id} not found."
            )

        if status is not None:
            task.status = status

        if priority is not None:
            task.priority = priority

        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "skill": task.skill,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()