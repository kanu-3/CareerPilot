from backend.tools.learning_tool import (
    create_learning_task,
    get_learning_tasks,
    update_learning_task,
)


USER_ID = 1


print("\n========== CREATE LEARNING TASK ==========")

task = create_learning_task(
    user_id=USER_ID,
    skill="LangChain",
    title="Learn LangChain Tool Calling",
    description=(
        "Learn how to create tools, bind tools to an LLM, "
        "and execute tool calls in an agent workflow."
    ),
    priority="high",
)

print(task)


print("\n========== GET LEARNING TASKS ==========")

tasks = get_learning_tasks(
    user_id=USER_ID,
)

for item in tasks:
    print(item)


print("\n========== UPDATE LEARNING TASK ==========")

task_id = task["task_id"]

updated = update_learning_task(
    user_id=USER_ID,
    task_id=task_id,
    status="in_progress",
)

print(updated)


print("\n========== VERIFY ==========")

tasks = get_learning_tasks(
    user_id=USER_ID,
)

for item in tasks:
    print(item)