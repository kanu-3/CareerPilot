from fastapi import APIRouter, HTTPException

from backend.agent.approval_manager import (
    get_approval,
    approve_action,
    reject_action,
)
from backend.agent.resume import resume_approved_run


router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("/{approval_id}")
def get_approval_status(approval_id: int):
    approval = get_approval(approval_id)

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail="Approval not found.",
        )

    return approval


@router.post("/{approval_id}/approve")
def approve(approval_id: int):
    try:
        return approve_action(approval_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/{approval_id}/reject")
def reject(approval_id: int):
    try:
        return reject_action(approval_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/{approval_id}/resume")
def resume(approval_id: int):
    try:
        return resume_approved_run(approval_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )