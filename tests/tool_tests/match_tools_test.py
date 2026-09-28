from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Job, User
from backend.tools.match_tool import analyze_job_match


db = SessionLocal()

try:
    user = db.execute(
        select(User).where(
            User.email == "test@careerpilot.local"
        )
    ).scalar_one()

    job = db.execute(
        select(Job).where(
            Job.title == "AI Engineer"
        )
    ).scalars().first()

    user_id = user.id
    job_id = job.id

finally:
    db.close()


result = analyze_job_match(
    job_id=job_id,
    user_id=user_id,
)


print("\n========== JOB MATCH ANALYSIS ==========\n")
print(result["analysis"])

print("\n========== RETRIEVED EVIDENCE ==========\n")

for item in result["evidence"]:
    print("--------------------")
    print("Section:", item["section"])
    print("Project:", item["project"])
    print("Source:", item["source_type"])
    print(item["content"])