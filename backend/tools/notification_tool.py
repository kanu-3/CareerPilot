from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Notification


VALID_TYPES = {
    "job",
    "learning",
    "application",
    "interview",
    "approval",
    "system",
}


def create_notification(
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
) -> dict:

    if notification_type not in VALID_TYPES:
        raise ValueError(
            f"Invalid notification type '{notification_type}'. "
            f"Valid types: {sorted(VALID_TYPES)}"
        )

    db = SessionLocal()

    try:
        notification = Notification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            is_read=False,
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return {
            "success": True,
            "notification_id": notification.id,
            "notification_type": notification.notification_type,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_notifications(
    user_id: int,
    unread_only: bool = False,
) -> list[dict]:

    db = SessionLocal()

    try:
        statement = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        if unread_only:
            statement = statement.where(
                Notification.is_read == False
            )

        notifications = db.execute(
            statement
        ).scalars().all()

        return [
            {
                "notification_id": notification.id,
                "notification_type": notification.notification_type,
                "title": notification.title,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at,
            }
            for notification in notifications
        ]

    finally:
        db.close()


def mark_notification_read(
    user_id: int,
    notification_id: int,
) -> dict:

    db = SessionLocal()

    try:
        notification = db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        ).scalar_one_or_none()

        if notification is None:
            raise ValueError(
                f"Notification {notification_id} not found."
            )

        notification.is_read = True

        db.commit()
        db.refresh(notification)

        return {
            "success": True,
            "notification_id": notification.id,
            "is_read": notification.is_read,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()