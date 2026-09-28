from backend.agent.run_manager import (
    create_agent_run,
    complete_agent_run,
)


run_id = create_agent_run(
    user_id=1,
    request="Test CareerPilot agent run.",
)

print("\n========== RUN CREATED ==========")
print("Run ID:", run_id)


complete_agent_run(
    run_id=run_id,
    decision="Test decision",
    explanation="Test explanation",
)

print("\n========== RUN COMPLETED ==========")
print("Run ID:", run_id)