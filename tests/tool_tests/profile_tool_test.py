from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import User
from backend.tools.profile_tool import get_profile


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


profile = get_profile(user_id)

print("\n========== PROFILE ==========\n")
print(profile)