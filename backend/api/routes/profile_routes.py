from fastapi import APIRouter, HTTPException

from backend.tools.profile_tool import (
    get_profile,
    get_skills,
)


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/{user_id}")
def profile(user_id: int):
    try:
        profile_data = get_profile(user_id)
        skills = get_skills(user_id)

        return {
            "profile": profile_data,
            "skills": skills,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )