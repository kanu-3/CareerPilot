import re


def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()

    replacements = {
        "postgres": "postgresql",
        "scikit learn": "scikit-learn",
        "scikitlearn": "scikit-learn",
        "machine-learning": "machine learning",
        "gen ai": "generative ai",
    }

    skill = replacements.get(skill, skill)

    skill = re.sub(r"\s+", " ", skill)

    return skill


def skill_in_text(skill: str, text: str) -> bool:
    normalized_skill = normalize_skill(skill)
    normalized_text = text.lower()

    pattern = rf"(?<!\w){re.escape(normalized_skill)}(?!\w)"

    return re.search(pattern, normalized_text) is not None


def find_skill_evidence(
    skill: str,
    knowledge: list[dict],
) -> list[dict]:

    matches = []

    for item in knowledge:

        if skill_in_text(
            skill,
            item["content"],
        ):
            matches.append(
                {
                    "skill": skill,
                    "content": item["content"],
                    "section": item["section"],
                    "project": item["project"],
                    "source_type": item["source_type"],
                    "document_id": item["document_id"],
                    "chunk_id": item["chunk_id"],
                }
            )

    return matches