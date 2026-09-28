from backend.agent.graph import agent_graph


initial_state = {
    "user_id": 1,
    "request": "Submit my application for the AI Engineer role.",
    "job_id": 1,
    "selected_tool": "submit_application",
}


result = agent_graph.invoke(initial_state)


print("\n========== APPROVAL FLOW ==========")
print("Run ID:", result.get("run_id"))
print("Selected Tool:", result.get("selected_tool"))
print("Approval Required:", result.get("approval_required"))
print("Approval Status:", result.get("approval_status"))

print("\n========== TOOL RESULT ==========")
print(result.get("tool_result"))

print("\n========== ERROR ==========")
print(result.get("error"))