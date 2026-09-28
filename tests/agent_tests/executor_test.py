from backend.agent.executor import execute_selected_tool


state = {
    "user_id": 1,
    "selected_tool": "create_learning_task",
    "tool_input": {
        "user_id": 1,
        "skill": "LangChain",
        "title": "Practice LangChain tool calling",
        "description": "Build and test a LangChain tool-calling workflow.",
        "priority": "high",
    },
}


result = execute_selected_tool(state)


print("\n========== EXECUTION RESULT ==========")
print(result.get("tool_result"))

print("\n========== ERROR ==========")
print(result.get("error"))