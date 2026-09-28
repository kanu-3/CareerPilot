def validate_reasoning(
    decision: str,
    skill_gaps: list[str],
) -> dict:
    return {
        "has_decision": bool(decision.strip()),
        "skill_gap_count": len(skill_gaps),
        "valid": bool(decision.strip()),
    }