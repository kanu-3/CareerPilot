from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User
from backend.tools.profile_tool import get_skills


db = SessionLocal()

try:
    user = db.execute(
        select(User).where(
            User.email == "test@careerpilot.local"
        )
    ).scalar_one()

    user_id = user.id

finally:
    db.close()


skills = get_skills(user_id)

print("\n========== SKILLS ==========\n")

for skill in skills:
    print("--------------------")
    print("Name:", skill["name"])
    print("Proficiency:", skill["proficiency"])
    print("Evidence:", skill["evidence"])
    print("Source:", skill["source"])
    print("Verified:", skill["verified"])