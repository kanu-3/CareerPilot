from backend.agent.nodes import (
    retrieve_profile,
    retrieve_job,
    retrieve_knowledge_node,
    retrieve_memories,
    retrieve_learning,
)

from backend.agent.reasoner import reason_about_job
from backend.agent.tool_selector import select_tool


state = {
    "user_id": 1,
    "job_id": 1,
    "request": "Analyze job 1 for my profile and identify my skill gaps.",
}


state = retrieve_profile(state)
state = retrieve_job(state)
state = retrieve_knowledge_node(state)
state = retrieve_memories(state)
state = retrieve_learning(state)

state = reason_about_job(state)
state = select_tool(state)


print("\n========== DECISION ==========")
print(state.get("decision"))

print("\n========== SKILL GAPS ==========")
print(state.get("skill_gaps"))

print("\n========== SELECTED TOOL ==========")
print(state.get("selected_tool"))

print("\n========== TOOL INPUT ==========")
print(state.get("tool_input"))

print("\n========== TOOL REASON ==========")
print(state.get("explanation"))