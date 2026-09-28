from backend.agent.nodes import (
    retrieve_profile,
    retrieve_job,
    retrieve_knowledge_node,
    retrieve_memories,
    retrieve_learning,
)


state = {
    "user_id": 1,
    "job_id": 1,
    "request": "Analyze job 1 for my profile and identify my skill gaps.",
}


state = retrieve_profile(state)

print("\n========== PROFILE ==========")
print(state["profile"])

print("\n========== SKILLS ==========")
print(state["skills"])


state = retrieve_job(state)

print("\n========== JOB ==========")
print(state["job"])


state = retrieve_knowledge_node(state)

print("\n========== KNOWLEDGE ==========")
print(f"Retrieved {len(state['knowledge'])} chunks")

for item in state["knowledge"]:
    print(
        f"- {item['section']} | "
        f"{item['project']} | "
        f"{item['content'][:100]}..."
    )


state = retrieve_memories(state)

print("\n========== MEMORIES ==========")
print(state["memories"])


state = retrieve_learning(state)

print("\n========== LEARNING ==========")
print(state["learning_tasks"])