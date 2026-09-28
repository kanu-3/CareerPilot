AUTONOMOUS_TOOLS = {
    "save_job",
    "create_learning_task",
    "update_learning_task",
    "save_memory",
    "create_notification",
    "update_application",
}


APPROVAL_REQUIRED_TOOLS = {
    "modify_final_resume",
    "send_recruiter_message",
    "submit_application",
}


ALL_ALLOWED_TOOLS = (
    AUTONOMOUS_TOOLS
    | APPROVAL_REQUIRED_TOOLS
)


def is_allowed_tool(tool_name: str) -> bool:
    return tool_name in ALL_ALLOWED_TOOLS


def requires_approval(tool_name: str) -> bool:
    return tool_name in APPROVAL_REQUIRED_TOOLS