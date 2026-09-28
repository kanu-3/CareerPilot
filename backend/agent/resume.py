from backend.agent.tool_registry import get_tool
from backend.agent.policies.tool_policy import is_allowed_tool
from backend.agent.run_manager import complete_agent_run
from backend.audit.logger import log_audit_event
from backend.database.connection import SessionLocal
from backend.database.model import AgentRun, Approval


def resume_approved_run(approval_id: int) -> dict:
    db = SessionLocal()

    try:
        approval = (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

        if approval is None:
            raise ValueError("Approval not found.")

        if approval.status != "approved":
            raise ValueError(
                f"Approval is not approved. Current status: {approval.status}"
            )

        run = (
            db.query(AgentRun)
            .filter(AgentRun.id == approval.run_id)
            .first()
        )

        if run is None:
            raise ValueError("Agent run not found.")

        tool_name = run.selected_tool
        tool_input = run.tool_input or {}

        if not tool_name:
            raise ValueError("No selected tool stored for this run.")

        if not is_allowed_tool(tool_name):
            raise ValueError(
                f"Tool is not allowed: {tool_name}"
            )

        tool = get_tool(tool_name)

        if tool is None:
            raise ValueError(
                f"Tool is not registered: {tool_name}"
            )

        log_audit_event(
            run_id=run.id,
            action="approved_action_execution_started",
            tool_name=tool_name,
            input_data=tool_input,
        )

        try:
            result = tool(**tool_input)

            log_audit_event(
                run_id=run.id,
                action="approved_action_executed",
                tool_name=tool_name,
                input_data=tool_input,
                output_data=result,
                status="success",
            )
            approval.status = "executed"
            db.commit()

            complete_agent_run(
                run_id=run.id,
                decision=run.decision,
                explanation=run.explanation,
                status="completed",
            )

            return {
                "success": True,
                "run_id": run.id,
                "approval_id": approval.id,
                "tool": tool_name,
                "tool_result": result,
                "status": "completed",
            }

        except Exception as exc:
            error_message = str(exc)

            log_audit_event(
                run_id=run.id,
                action="approved_action_execution_failed",
                tool_name=tool_name,
                input_data=tool_input,
                output_data={
                    "error": error_message,
                },
                status="failed",
            )

            complete_agent_run(
                run_id=run.id,
                decision=run.decision,
                explanation=run.explanation,
                status="failed",
            )

            raise

    finally:
        db.close()