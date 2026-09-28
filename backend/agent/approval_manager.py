from datetime import datetime

from backend.database.connection import SessionLocal
from backend.database.model import Approval
from backend.audit.logger import log_audit_event


def get_approval(approval_id: int):
    db = SessionLocal()

    try:
        approval = (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

        if approval is None:
            return None

        return {
            "id": approval.id,
            "run_id": approval.run_id,
            "action": approval.action,
            "description": approval.description,
            "status": approval.status,
            "created_at": approval.created_at,
            "approved_at": approval.approved_at,
        }

    finally:
        db.close()


def approve_action(approval_id: int):
    db = SessionLocal()

    try:
        approval = (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

        if approval is None:
            raise ValueError("Approval not found.")

        if approval.status != "pending":
            raise ValueError(
                f"Approval is already {approval.status}."
            )

        approval.status = "approved"
        approval.approved_at = datetime.utcnow()

        db.commit()
        db.refresh(approval)

        log_audit_event(
            run_id=approval.run_id,
            action="approval_granted",
            tool_name=approval.action,
            output_data={
                "approval_id": approval.id,
                "status": "approved",
            },
        )

        return {
            "success": True,
            "approval_id": approval.id,
            "run_id": approval.run_id,
            "action": approval.action,
            "status": approval.status,
        }

    finally:
        db.close()


def reject_action(approval_id: int):
    db = SessionLocal()

    try:
        approval = (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

        if approval is None:
            raise ValueError("Approval not found.")

        if approval.status != "pending":
            raise ValueError(
                f"Approval is already {approval.status}."
            )

        approval.status = "rejected"

        db.commit()
        db.refresh(approval)

        log_audit_event(
            run_id=approval.run_id,
            action="approval_rejected",
            tool_name=approval.action,
            output_data={
                "approval_id": approval.id,
                "status": "rejected",
            },
            status="rejected",
        )

        return {
            "success": True,
            "approval_id": approval.id,
            "run_id": approval.run_id,
            "action": approval.action,
            "status": approval.status,
        }

    finally:
        db.close()