from backend.agent.policies.tool_policy import (
    is_allowed_tool,
    requires_approval,
)


tools = [
    "save_job",
    "create_learning_task",
    "submit_application",
    "send_recruiter_message",
    "unknown_tool",
]


for tool in tools:
    print(
        tool,
        "| allowed =", is_allowed_tool(tool),
        "| approval =", requires_approval(tool),
    )