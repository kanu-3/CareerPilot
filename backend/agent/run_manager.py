from datetime import datetime

from backend.database.connection import SessionLocal
from backend.database.model import AgentRun


def create_agent_run(
    user_id: int,
    request: str,
    selected_tool: str | None = None,
    tool_input: dict | None = None,
) -> int:
    db = SessionLocal()

    try:
        run = AgentRun(
            user_id=user_id,
            request=request,
            status="started",
            selected_tool=selected_tool,
            tool_input=tool_input,
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        return run.id

    finally:
        db.close()

def update_agent_run_action(
    run_id: int,
    selected_tool: str,
    tool_input: dict,
):
    db = SessionLocal()

    try:
        run = (
            db.query(AgentRun)
            .filter(AgentRun.id == run_id)
            .first()
        )

        if run is None:
            raise ValueError("Agent run not found.")

        run.selected_tool = selected_tool
        run.tool_input = tool_input

        db.commit()

    finally:
        db.close()

        
def complete_agent_run(
    run_id: int,
    decision: str | None = None,
    explanation: str | None = None,
    status: str = "completed",
):
    db = SessionLocal()

    try:
        run = db.query(AgentRun).filter(
            AgentRun.id == run_id
        ).first()

        if run is None:
            return

        run.status = status
        run.decision = decision
        run.explanation = explanation
        run.completed_at = datetime.utcnow()

        db.commit()

    finally:
        db.close()

def update_agent_run_reasoning(
    run_id: int,
    decision: str | None,
    explanation: str | None,
):
    db = SessionLocal()
    try:
        run = (
            db.query(AgentRun)
            .filter(AgentRun.id == run_id)
            .first()
        )

        if run is None:
            raise ValueError("Agent run not found.")

        run.decision = decision
        run.explanation = explanation

        db.commit()
    finally:
        db.close()