from backend.agent.approval import check_tool_approval


safe_state = {
    "selected_tool": "create_learning_task",
}

safe_result = check_tool_approval(safe_state)

print("\n========== SAFE ACTION ==========")
print("Tool:", safe_result["selected_tool"])
print("Approval required:", safe_result["approval_required"])
print("Approval status:", safe_result["approval_status"])


critical_state = {
    "selected_tool": "submit_application",
}

critical_result = check_tool_approval(critical_state)

print("\n========== CRITICAL ACTION ==========")
print("Tool:", critical_result["selected_tool"])
print("Approval required:", critical_result["approval_required"])
print("Approval action:", critical_result["approval_action"])
print("Approval description:", critical_result["approval_description"])
print("Approval status:", critical_result["approval_status"])