from backend.tools.application_tool import (
    create_application,
    get_applications,
    get_application,
    update_application,
)


USER_ID = 1
JOB_ID = 1


print("\n========== CREATE APPLICATION ==========")

application = create_application(
    user_id=USER_ID,
    job_id=JOB_ID,
    resume_version="master_resume_v1",
    notes="Potential AI Engineer opportunity.",
)

print(application)


if not application["success"]:
    application_id = application["application_id"]
else:
    application_id = application["application_id"]


print("\n========== GET APPLICATIONS ==========")

applications = get_applications(
    user_id=USER_ID,
)

for item in applications:
    print(item)


print("\n========== GET ONE APPLICATION ==========")

one_application = get_application(
    user_id=USER_ID,
    application_id=application_id,
)

print(one_application)


print("\n========== UPDATE APPLICATION ==========")

updated = update_application(
    user_id=USER_ID,
    application_id=application_id,
    status="applied",
    interview_status="not_started",
    notes="Application submitted.",
)

print(updated)


print("\n========== VERIFY ==========")

one_application = get_application(
    user_id=USER_ID,
    application_id=application_id,
)

print(one_application)