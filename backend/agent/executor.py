from backend.agent.state import AgentState
from backend.agent.tool_registry import get_tool
from backend.agent.policies.tool_policy import is_allowed_tool


def execute_selected_tool(state: AgentState) -> AgentState:
    tool_name = state.get("selected_tool", "none")

    if tool_name == "none":
        state["tool_result"] = {
            "status": "no_action",
            "message": "No tool was selected.",
        }
        return state

    if not is_allowed_tool(tool_name):
        state["error"] = f"Tool is not allowed: {tool_name}"
        return state

    tool = get_tool(tool_name)

    if tool is None:
        state["error"] = f"Tool is not registered: {tool_name}"
        return state

    tool_input = state.get("tool_input", {})

    try:
        result = tool(**tool_input)

        state["tool_result"] = {
            "status": "success",
            "tool": tool_name,
            "result": result,
        }

    except Exception as exc:
        state["tool_result"] = {
            "status": "error",
            "tool": tool_name,
            "error": str(exc),
        }

        state["error"] = str(exc)

    return state