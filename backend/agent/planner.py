import json

from backend.agent.state import AgentState
from backend.llm.qwen import qwen_model
from backend.agent.prompts.planner_prompt import PLANNER_SYSTEM_PROMPT

def create_plan(state: AgentState) -> AgentState:
    request = state["request"]

    prompt = f"""
Create an execution plan for this CareerPilot request:

REQUEST:
{request}

Return JSON only.
"""

    raw_response = qwen_model.generate(
        prompt=prompt,
        system_prompt=PLANNER_SYSTEM_PROMPT,
    )

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError:
        start = raw_response.find("{")
        end = raw_response.rfind("}")

        if start == -1 or end == -1:
            state["error"] = "Planner did not return valid JSON."
            return state

        result = json.loads(raw_response[start:end + 1])

    state["intent"] = result.get("intent", "")
    state["plan"] = result.get("plan", [])

    if state["plan"]:
        state["current_step"] = state["plan"][0]

    return state