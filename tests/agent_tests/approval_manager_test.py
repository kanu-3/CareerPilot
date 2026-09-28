from backend.agent.approval_manager import (
    get_approval,
    approve_action,
)


approval_id = 1

print("\n========== BEFORE APPROVAL ==========")
print(get_approval(approval_id))


result = approve_action(approval_id)

print("\n========== APPROVED ==========")
print(result)


print("\n========== AFTER APPROVAL ==========")
print(get_approval(approval_id))