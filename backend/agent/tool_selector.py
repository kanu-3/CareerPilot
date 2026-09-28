import json

from backend.agent.state import AgentState
from backend.agent.prompts.tool_selector_prompt import (
    TOOL_SELECTOR_SYSTEM_PROMPT,
)
from backend.llm.qwen import qwen_model


AVAILABLE_TOOLS = [
    {
        "name": "save_job",
        "description": "Save a job to the user's saved jobs.",
    },
    {
        "name": "create_learning_task",
        "description": "Create a learning task for a skill gap.",
    },
    {
        "name": "update_learning_task",
        "description": "Update the status or priority of an existing learning task.",
    },
    {
        "name": "save_memory",
        "description": "Persist useful long-term career context, preferences, goals, or decisions.",
    },
    {
        "name": "create_notification",
        "description": "Create an internal notification for the user.",
    },
    {
        "name": "update_application",
        "description": "Update an existing job application record.",
    },
    {
        "name": "submit_application",
        "description": "Submit the user's application for a specific job using the selected resume version. This action requires human approval before execution.",
    },
]


def normalize_tool_input(tool_name: str, tool_input: dict) -> dict:
    allowed_arguments = {
        "save_job": {
            "user_id",
            "job_id",
            "notes",
        },
        "create_learning_task": {
            "user_id",
            "skill",
            "title",
            "description",
            "priority",
            "resource_url",
            "due_date",
        },
        "update_learning_task": {
            "user_id",
            "task_id",
            "status",
            "priority",
        },
        "save_memory": {
            "user_id",
            "memory_type",
            "content",
            "importance",
        },
        "create_notification": {
            "user_id",
            "notification_type",
            "title",
            "message",
        },
        "update_application": {
            "user_id",
            "application_id",
            "status",
            "interview_status",
            "notes",
            "outcome",
        },
        "submit_application": {
            "user_id",
            "job_id",
            "resume_version",
        },
    }

    allowed = allowed_arguments.get(tool_name)

    if allowed is None:
        return tool_input

    return {
        key: value
        for key, value in tool_input.items()
        if key in allowed
    }


def select_tool(state: AgentState) -> AgentState:
    request = state.get("request", "")
    intent = state.get("intent", "")
    plan = state.get("plan", [])

    analysis = state.get("analysis", {})
    decision = state.get("decision", "")
    skill_gaps = state.get("skill_gaps", [])

    available_tools = json.dumps(
        AVAILABLE_TOOLS,
        indent=2,
    )

    prompt = f"""
Select the appropriate tool for the current CareerPilot request.

USER REQUEST:
{request}

PLANNED INTENT:
{intent}

EXECUTION PLAN:
{json.dumps(plan, indent=2, default=str)}

DECISION:
{decision}

ANALYSIS:
{json.dumps(analysis, indent=2, default=str)}

SKILL GAPS:
{json.dumps(skill_gaps, indent=2, default=str)}

AVAILABLE TOOLS:
{available_tools}

CURRENT STATE:
{json.dumps({
    "user_id": state.get("user_id"),
    "job_id": state.get("job_id"),
    "job": state.get("job"),
    "learning_tasks": state.get("learning_tasks"),
}, indent=2, default=str)}

IMPORTANT:
The planned intent represents the user's primary requested action.

If the planned intent explicitly corresponds to an available tool,
select that tool.

Do NOT replace an explicit user action with a learning task,
recommendation, notification, or another tool.

For example:

planned intent = "submit_application"
-> select "submit_application"

planned intent = "save_job"
-> select "save_job"

planned intent = "create_learning_task"
-> select "create_learning_task"

A skill gap must NOT override an explicit user-requested action.

Return JSON only.
"""

    raw_response = qwen_model.generate(
        prompt=prompt,
        system_prompt=TOOL_SELECTOR_SYSTEM_PROMPT,
    )

    try:
        result = json.loads(raw_response)

    except json.JSONDecodeError:
        start = raw_response.find("{")
        end = raw_response.rfind("}")

        if start == -1 or end == -1:
            state["error"] = "Tool selector did not return valid JSON."
            return state

        result = json.loads(raw_response[start:end + 1])

    selected_tool = result.get("tool", "none")

    valid_tool_names = {
        tool["name"]
        for tool in AVAILABLE_TOOLS
    }

    if selected_tool != "none" and selected_tool not in valid_tool_names:
        state["error"] = f"Invalid tool selected: {selected_tool}"
        return state

    state["selected_tool"] = selected_tool

    raw_tool_input = result.get("arguments", {})

    state["tool_input"] = normalize_tool_input(
        selected_tool,
        raw_tool_input,
    )

    state["explanation"] = result.get(
        "reason",
        state.get("explanation", ""),
    )

    return state