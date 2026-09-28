from backend.agent.graph import agent_graph


initial_state = {
    "user_id": 1,
    "request": "Analyze my fit for the AI Engineer job and identify my skill gaps.",
    "job_id": 1,
}


result = agent_graph.invoke(initial_state)


print("\n========== AGENT RUN ==========")
print("Run ID:", result.get("run_id"))

print("\n========== DECISION ==========")
print(result.get("decision"))

print("\n========== EXPLANATION ==========")
print(result.get("explanation"))

print("\n========== SELECTED TOOL ==========")
print(result.get("selected_tool"))

print("\n========== TOOL RESULT ==========")
print(result.get("tool_result"))

print("\n========== ERROR ==========")
print(result.get("error"))