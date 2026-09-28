from backend.agent.approval import (
    check_tool_approval,
    create_approval_request,
)
from backend.agent.run_manager import create_agent_run


run_id = create_agent_run(
    user_id=1,
    request="Test approval for submitting an application.",
)

state = {
    "user_id": 1,
    "request": "Submit my application for the AI Engineer role.",
    "run_id": run_id,
    "selected_tool": "submit_application",
}


state = check_tool_approval(state)

print("\n========== APPROVAL CHECK ==========")
print("Approval Required:", state.get("approval_required"))
print("Approval Action:", state.get("approval_action"))
print("Approval Status:", state.get("approval_status"))


state = create_approval_request(state)

print("\n========== APPROVAL CREATED ==========")
print(state.get("tool_result"))
print("Error:", state.get("error"))