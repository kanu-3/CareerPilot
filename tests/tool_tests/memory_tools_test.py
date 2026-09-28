from backend.tools.memory_tool import (
    save_memory,
    get_memories,
    get_memory,
    update_memory,
)


USER_ID = 1


print("\n========== SAVE MEMORY ==========")

memory = save_memory(
    user_id=USER_ID,
    memory_type="preference",
    content="Prefers AI/ML and AI engineering roles.",
    importance="high",
)

print(memory)


memory_id = memory["memory_id"]


print("\n========== GET MEMORIES ==========")

memories = get_memories(
    user_id=USER_ID,
)

for item in memories:
    print(item)


print("\n========== GET ONE MEMORY ==========")

one_memory = get_memory(
    user_id=USER_ID,
    memory_id=memory_id,
)

print(one_memory)


print("\n========== UPDATE MEMORY ==========")

updated = update_memory(
    user_id=USER_ID,
    memory_id=memory_id,
    content="Targets AI Engineer, ML Engineer, and GenAI Engineer roles.",
)

print(updated)


print("\n========== VERIFY ==========")

one_memory = get_memory(
    user_id=USER_ID,
    memory_id=memory_id,
)

print(one_memory)