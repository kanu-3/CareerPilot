from backend.agent.lifecycle import (
    start_agent_run,
    finalize_agent_run,
)


state = {
    "user_id": 1,
    "request": "Find my skill gaps for this job.",
    "decision": "Create a LangChain learning task.",
    "explanation": "LangChain is required but currently has limited evidence.",
    "selected_tool": "create_learning_task",
    "tool_result": {
        "status": "success",
        "task_id": 1,
    },
}


state = start_agent_run(state)

print("\n========== RUN STARTED ==========")
print("Run ID:", state["run_id"])


state = finalize_agent_run(state)

print("\n========== RUN FINALIZED ==========")
print("Run ID:", state["run_id"])