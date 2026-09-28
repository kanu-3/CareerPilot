from backend.tools.job_management_tool import (
    save_job,
    get_saved_jobs,
    get_saved_job,
    update_job_status,
    remove_saved_job,
)


USER_ID = 1
JOB_ID = 1


print("\n========== SAVE JOB ==========")

result = save_job(
    user_id=USER_ID,
    job_id=JOB_ID,
    notes="Potential AI Engineer opportunity.",
)

print(result)


print("\n========== GET SAVED JOBS ==========")

saved_jobs = get_saved_jobs(
    user_id=USER_ID,
)

for job in saved_jobs:
    print(job)


print("\n========== GET ONE SAVED JOB ==========")

saved_job = get_saved_job(
    user_id=USER_ID,
    job_id=JOB_ID,
)

print(saved_job)


print("\n========== UPDATE STATUS ==========")

updated = update_job_status(
    user_id=USER_ID,
    job_id=JOB_ID,
    status="considering",
)

print(updated)


print("\n========== VERIFY STATUS ==========")

saved_job = get_saved_job(
    user_id=USER_ID,
    job_id=JOB_ID,
)

print(saved_job)


# Uncomment this after the above works if you want
# to test removal.

# print("\n========== REMOVE JOB ==========")
#
# removed = remove_saved_job(
#     user_id=USER_ID,
#     job_id=JOB_ID,
# )
#
# print(removed)