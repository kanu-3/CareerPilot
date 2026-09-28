from backend.agent.graph import agent_graph


state = {
    "user_id": 1,
    "job_id": 1,
    "request": "Submit my application for this job.",
}


result = agent_graph.invoke(state)


print("\n========== SELECTED TOOL ==========")
print(result.get("selected_tool"))

print("\n========== APPROVAL REQUIRED ==========")
print(result.get("approval_required"))

print("\n========== APPROVAL STATUS ==========")
print(result.get("approval_status"))

print("\n========== TOOL RESULT ==========")
print(result.get("tool_result"))

print("\n========== ERROR ==========")
print(result.get("error"))