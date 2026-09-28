import json

from backend.agent.state import AgentState
from backend.agent.prompts.reasoner_prompt import REASONER_SYSTEM_PROMPT
from backend.llm.qwen import qwen_model
from backend.agent.run_manager import update_agent_run_reasoning


def reason_about_job(state: AgentState) -> AgentState:
    request = state.get("request", "")
    intent = state.get("intent", "")
    plan = state.get("plan", [])

    profile = state.get("profile", {})
    skills = state.get("skills", [])
    job = state.get("job", {})
    knowledge = state.get("knowledge", [])
    memories = state.get("memories", [])
    learning_tasks = state.get("learning_tasks", [])

    prompt = f"""
Analyze the user's request and the retrieved career information.

USER REQUEST:
{request}

PLANNED INTENT:
{intent}

EXECUTION PLAN:
{json.dumps(plan, indent=2, default=str)}

IMPORTANT:
The user's explicit requested action is authoritative.

If the planned intent is an explicit action such as
"submit_application", do not replace it with a learning recommendation.

You may identify missing information or prerequisites, but your decision
must address the user's requested action.

PROFILE:
{json.dumps(profile, indent=2, default=str)}

STRUCTURED SKILLS:
{json.dumps(skills, indent=2, default=str)}

JOB:
{json.dumps(job, indent=2, default=str)}

KNOWLEDGE EVIDENCE:
{json.dumps(knowledge, indent=2, default=str)}

LONG-TERM MEMORIES:
{json.dumps(memories, indent=2, default=str)}

LEARNING TASKS:
{json.dumps(learning_tasks, indent=2, default=str)}

Determine:

1. What evidence exists for the job requirements?
2. Which requirements have missing or insufficient evidence?
3. What concrete skill gaps exist?
4. What should CareerPilot do next while respecting the user's explicit intent?
5. Explain the decision using the retrieved evidence.

Return JSON only.
"""

    raw_response = qwen_model.generate(
        prompt=prompt,
        system_prompt=REASONER_SYSTEM_PROMPT,
    )

    try:
        analysis = json.loads(raw_response)

    except json.JSONDecodeError:
        start = raw_response.find("{")
        end = raw_response.rfind("}")

        if start == -1 or end == -1:
            state["error"] = "Reasoning model did not return valid JSON."
            return state

        analysis = json.loads(raw_response[start:end + 1])

    state["decision"] = analysis.get("decision", "")
    state["explanation"] = analysis.get("explanation", "")
    state["skill_gaps"] = analysis.get("skill_gaps", [])
    state["analysis"] = analysis

    if state.get("run_id") is not None:
        update_agent_run_reasoning(
            run_id=state["run_id"],
            decision=state.get("decision"),
            explanation=state.get("explanation"),
        )

    return state