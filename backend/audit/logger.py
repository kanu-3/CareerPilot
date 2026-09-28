from datetime import datetime

from backend.database.connection import SessionLocal
from backend.database.model import AuditLog


def log_audit_event(
    run_id: int,
    action: str,
    tool_name: str | None = None,
    input_data: dict | None = None,
    output_data: dict | None = None,
    status: str = "success",
):
    db = SessionLocal()

    try:
        event = AuditLog(
            run_id=run_id,
            action=action,
            tool_name=tool_name,
            input_data=input_data,
            output_data=output_data,
            status=status,
            created_at=datetime.utcnow(),
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return event.id

    finally:
        db.close()