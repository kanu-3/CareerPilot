from backend.agent.run_manager import create_agent_run
from backend.audit.logger import log_audit_event


run_id = create_agent_run(
    user_id=1,
    request="Test audit logging.",
)

audit_id = log_audit_event(
    run_id=run_id,
    action="test_action",
    tool_name="create_learning_task",
    input_data={
        "skill": "LangGraph",
        "title": "Learn LangGraph workflows",
    },
    output_data={
        "status": "success",
        "task_id": 123,
    },
)

print("\n========== AUDIT EVENT CREATED ==========")
print("Run ID:", run_id)
print("Audit ID:", audit_id)