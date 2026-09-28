from backend.agent.state import AgentState
from backend.agent.run_manager import create_agent_run, complete_agent_run
from backend.audit.logger import log_audit_event


def start_agent_run(state: AgentState) -> AgentState:
    user_id = state["user_id"]
    request = state["request"]

    run_id = create_agent_run(
        user_id=user_id,
        request=request,
    )

    state["run_id"] = run_id
    state["audit_events"] = []

    log_audit_event(
        run_id=run_id,
        action="agent_started",
        input_data={
            "request": request,
        },
        output_data={
            "status": "started",
        },
    )

    return state


def finalize_agent_run(state: AgentState) -> AgentState:
    run_id = state.get("run_id")

    if run_id is None:
        return state

    status = "failed" if state.get("error") else "completed"

    complete_agent_run(
        run_id=run_id,
        decision=state.get("decision"),
        explanation=state.get("explanation"),
        status=status,
    )

    log_audit_event(
        run_id=run_id,
        action="agent_completed",
        output_data={
            "status": status,
            "decision": state.get("decision"),
            "tool": state.get("selected_tool"),
            "tool_result": state.get("tool_result"),
        },
        status=status,
    )

    return state