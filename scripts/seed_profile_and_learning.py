import json
from pathlib import Path

from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import (
    User,
    Skill,
    Project,
    LearningTask,
)


BASE_DIR = Path(__file__).resolve().parent.parent
SEED_DIR = BASE_DIR / "data" / "seed"

PROFILE_FILE = SEED_DIR / "profile.json"
LEARNING_FILE = SEED_DIR / "learning.json"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_profile(db, data: dict) -> User:
    profile = data["user"]

    existing_user = db.execute(
        select(User).where(
            User.email == profile["email"]
        )
    ).scalar_one_or_none()

    if existing_user is not None:
        user = existing_user

        user.name = profile["name"]
        user.location = profile.get("location")
        user.target_roles = profile.get("target_roles")
        user.preferred_locations = profile.get(
            "preferred_locations"
        )
        user.salary_expectation = profile.get(
            "salary_expectation"
        )
        user.work_preference = profile.get(
            "work_preference"
        )
        user.education = profile.get("education")
        user.experience = profile.get("experience")
        user.career_goals = profile.get(
            "career_goals"
        )

        print(f"Updated existing user: {user.email}")

    else:
        user = User(
            name=profile["name"],
            email=profile["email"],
            location=profile.get("location"),
            target_roles=profile.get("target_roles"),
            preferred_locations=profile.get(
                "preferred_locations"
            ),
            salary_expectation=profile.get(
                "salary_expectation"
            ),
            work_preference=profile.get(
                "work_preference"
            ),
            education=profile.get("education"),
            experience=profile.get("experience"),
            career_goals=profile.get(
                "career_goals"
            ),
        )

        db.add(user)
        db.flush()

        print(f"Created user: {user.email}")

    db.flush()

    # ---------------------------------------------------------
    # Skills
    # ---------------------------------------------------------

    skills = data.get("skills", [])

    for skill_data in skills:

        existing_skill = db.execute(
            select(Skill).where(
                Skill.user_id == user.id,
                Skill.name == skill_data["name"],
            )
        ).scalar_one_or_none()

        if existing_skill is not None:
            existing_skill.proficiency = skill_data.get(
                "proficiency"
            )
            existing_skill.evidence = skill_data.get(
                "evidence"
            )
            existing_skill.source = skill_data.get(
                "source"
            )
            existing_skill.verified = skill_data.get(
                "verified",
                False,
            )

        else:
            skill = Skill(
                user_id=user.id,
                name=skill_data["name"],
                proficiency=skill_data.get(
                    "proficiency"
                ),
                evidence=skill_data.get(
                    "evidence"
                ),
                source=skill_data.get(
                    "source"
                ),
                verified=skill_data.get(
                    "verified",
                    False,
                ),
            )

            db.add(skill)

    print(f"Processed {len(skills)} skills.")

    # ---------------------------------------------------------
    # Projects
    # ---------------------------------------------------------

    projects = data.get("projects", [])

    for project_data in projects:

        existing_project = db.execute(
            select(Project).where(
                Project.user_id == user.id,
                Project.name == project_data["name"],
            )
        ).scalar_one_or_none()

        if existing_project is not None:
            existing_project.description = project_data.get(
                "description"
            )
            existing_project.technologies = project_data.get(
                "technologies"
            )
            existing_project.responsibilities = project_data.get(
                "responsibilities"
            )

        else:
            project = Project(
                user_id=user.id,
                name=project_data["name"],
                description=project_data.get(
                    "description"
                ),
                technologies=project_data.get(
                    "technologies"
                ),
                responsibilities=project_data.get(
                    "responsibilities"
                ),
            )

            db.add(project)

    print(f"Processed {len(projects)} projects.")

    return user


def seed_learning(db, user: User, data: dict):

    learning_tasks = data.get(
        "learning_tasks",
        [],
    )

    added = 0
    skipped = 0

    for task_data in learning_tasks:

        existing_task = db.execute(
            select(LearningTask).where(
                LearningTask.user_id == user.id,
                LearningTask.skill == task_data["skill"],
                LearningTask.title == task_data["title"],
            )
        ).scalar_one_or_none()

        if existing_task is not None:
            existing_task.description = task_data.get(
                "description"
            )
            existing_task.priority = task_data.get(
                "priority",
                "medium",
            )
            existing_task.status = task_data.get(
                "status",
                "pending",
            )
            existing_task.resource_url = task_data.get(
                "resource_url"
            )

            skipped += 1
            continue

        task = LearningTask(
            user_id=user.id,
            skill=task_data["skill"],
            title=task_data["title"],
            description=task_data["description"],
            priority=task_data.get(
                "priority",
                "medium",
            ),
            status=task_data.get(
                "status",
                "pending",
            ),
            resource_url=task_data.get(
                "resource_url"
            ),
        )

        db.add(task)
        added += 1

    print(
        f"Learning tasks: added={added}, "
        f"updated/existing={skipped}"
    )


def main():

    print("\n========== CAREERPILOT SEED ==========\n")

    profile_data = load_json(PROFILE_FILE)
    learning_data = load_json(LEARNING_FILE)

    db = SessionLocal()

    try:

        user = seed_profile(
            db=db,
            data=profile_data,
        )

        seed_learning(
            db=db,
            user=user,
            data=learning_data,
        )

        db.commit()

        print("\nSeed completed successfully.")

        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()