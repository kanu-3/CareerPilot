from backend.agent.resume import resume_approved_run


result = resume_approved_run(
    approval_id=2,
)

print("\n========== RESUMED RUN ==========")
print(result)