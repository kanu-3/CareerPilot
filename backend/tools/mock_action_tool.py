def mock_submit_application(
    user_id: int,
    job_id: int,
    resume_version: str | None = None,
):
    return {
        "success": True,
        "message": "Mock application submitted successfully.",
        "user_id": user_id,
        "job_id": job_id,
        "resume_version": resume_version,
    }