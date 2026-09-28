from backend.agent.state import AgentState


state: AgentState = {
    "user_id": 1,
    "request": "Analyze this AI Engineer job and identify my skill gaps.",
    "intent": "job_analysis",
    "plan": [
        "Retrieve job",
        "Retrieve profile",
        "Retrieve evidence",
        "Analyze requirements",
        "Identify skill gaps",
    ],
    "current_step": "Retrieve job",
    "approval_required": False,
    "approval_status": "not_required",
    "audit_events": [],
}


print("\n========== AGENT STATE ==========")

for key, value in state.items():
    print(f"{key}: {value}")