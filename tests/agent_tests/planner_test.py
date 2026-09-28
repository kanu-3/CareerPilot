from backend.agent.state import AgentState
from backend.agent.planner import create_plan


state: AgentState = {
    "user_id": 1,
    "request": (
        "Analyze job 1 against my profile, "
        "identify my skill gaps, and suggest "
        "what I should learn."
    ),
}


print("\n========== PLANNER TEST ==========")

result = create_plan(state)

print("\nIntent:")
print(result.get("intent"))

print("\nPlan:")

for index, step in enumerate(
    result.get("plan", []),
    start=1,
):
    print(f"{index}. {step}")

print("\nCurrent step:")
print(result.get("current_step"))