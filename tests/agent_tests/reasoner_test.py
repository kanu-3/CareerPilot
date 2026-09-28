from backend.agent.nodes import (
    retrieve_profile,
    retrieve_job,
    retrieve_knowledge_node,
    retrieve_memories,
    retrieve_learning,
)

from backend.agent.reasoner import reason_about_job


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


print("\n========== DECISION ==========")
print(state["decision"])

print("\n========== EXPLANATION ==========")
print(state["explanation"])

print("\n========== SKILL GAPS ==========")
print(state["skill_gaps"])

print("\n========== FULL ANALYSIS ==========")
print(state["analysis"])