from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_id: int
    request: str
    job_id: int | None

    intent: str
    plan: list[str]
    current_step: str

    profile: dict[str, Any]
    skills: list[dict[str, Any]]
    job: dict[str, Any]
    knowledge: list[dict[str, Any]]
    memories: list[dict[str, Any]]
    learning_tasks: list[dict[str, Any]]

    analysis: dict[str, Any]
    skill_gaps: list[str]

    decision: str
    explanation: str

    selected_tool: str
    tool_input: dict[str, Any]
    tool_result: dict[str, Any]

    approval_required: bool
    approval_action: str
    approval_description: str
    approval_status: str

    response: str
    run_id: int | None
    audit_events: list[dict[str, Any]]

    error: str | None