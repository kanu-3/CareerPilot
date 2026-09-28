from backend.agent.approval import (
    check_tool_approval,
    create_approval_request,
)
from backend.agent.approval_manager import approve_action
from backend.agent.resume import resume_approved_run
from backend.agent.run_manager import create_agent_run


state = {
    "user_id": 1,
    "request": "Submit my application for the AI Engineer role.",
    "selected_tool": "submit_application",
    "tool_input": {
        "user_id": 1,
        "job_id": 1,
        "resume_version": "master",
    },
}


run_id = create_agent_run(
    user_id=state["user_id"],
    request=state["request"],
)

state["run_id"] = run_id


state = check_tool_approval(state)

print("\n========== APPROVAL CHECK ==========")
print("Run ID:", run_id)
print("Approval Required:", state.get("approval_required"))
print("Approval Action:", state.get("approval_action"))


state = create_approval_request(state)

approval_id = state["tool_result"]["approval_id"]

print("\n========== APPROVAL CREATED ==========")
print("Approval ID:", approval_id)
print("Tool Input:", state["tool_input"])


approval = approve_action(approval_id)

print("\n========== APPROVED ==========")
print(approval)


result = resume_approved_run(approval_id)

print("\n========== RESUMED ==========")
print(result)