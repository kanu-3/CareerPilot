from backend.agent.state import AgentState
from backend.agent.policies.approval_policy import check_approval_required
from backend.agent.run_manager import update_agent_run_action
from backend.database.connection import SessionLocal
from backend.database.model import Approval
from backend.audit.logger import log_audit_event


def check_tool_approval(state: AgentState) -> AgentState:
    tool_name = state.get("selected_tool", "none")

    approval_required = check_approval_required(tool_name)

    state["approval_required"] = approval_required

    if not approval_required:
        state["approval_status"] = "not_required"
        return state

    state["approval_action"] = tool_name
    state["approval_description"] = (
        f"CareerPilot wants to execute the '{tool_name}' action."
    )
    state["approval_status"] = "pending"

    return state


def create_approval_request(state: AgentState) -> AgentState:
    if not state.get("approval_required"):
        return state

    run_id = state.get("run_id")

    if run_id is None:
        state["error"] = "Cannot create approval without a run_id."
        return state

    try:
        update_agent_run_action(
            run_id=run_id,
            selected_tool=state["selected_tool"],
            tool_input=state.get("tool_input", {}),
        )
    except Exception as exc:
        state["error"] = str(exc)
        return state

    db = SessionLocal()

    try:
        approval = Approval(
            run_id=run_id,
            action=state["approval_action"],
            description=state["approval_description"],
            status="pending",
        )

        db.add(approval)
        db.commit()
        db.refresh(approval)

        state["approval_status"] = "pending"

        state["tool_result"] = {
            "status": "approval_required",
            "approval_id": approval.id,
            "action": approval.action,
            "description": approval.description,
        }

        log_audit_event(
            run_id=run_id,
            action="approval_requested",
            tool_name=state["selected_tool"],
            input_data=state.get("tool_input", {}),
            output_data={
                "approval_id": approval.id,
                "action": approval.action,
                "description": approval.description,
                "status": "pending",
            },
        )

    except Exception as exc:
        db.rollback()
        state["error"] = str(exc)

    finally:
        db.close()

    return state