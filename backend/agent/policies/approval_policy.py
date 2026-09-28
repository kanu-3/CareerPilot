from backend.agent.policies.tool_policy import requires_approval


def check_approval_required(tool_name: str) -> bool:
    return requires_approval(tool_name)