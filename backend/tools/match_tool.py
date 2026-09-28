import json

from backend.llm.qwen import qwen_model
from backend.rag.retriever import retrieve_knowledge
from backend.tools.jobs_tool import get_job
from backend.tools.profile_tool import get_profile, get_skills
from backend.tools.evidence_tool import find_skill_evidence
from backend.schemas.match import JobMatchAnalysis


MATCH_SYSTEM_PROMPT = """
You are CareerPilot's job matching explanation engine.

The factual skill assessments have already been determined by
a deterministic evidence-matching system.

Your job is ONLY to explain those facts.

Rules:
1. Never change a supplied skill status.
2. Never invent skills, projects, experience, education, or qualifications.
3. Do not add skills that are not present in the supplied assessments.
4. Use only the supplied facts.
5. If something is unknown, say unknown.
6. Keep the explanation concise.
7. Return valid JSON only.
"""


def analyze_job_match(
    job_id: int,
    user_id: int,
) -> dict:

    # ---------------------------------------------------------
    # 1. Get job
    # ---------------------------------------------------------

    job = get_job(job_id)

    if job is None:
        raise ValueError(f"Job {job_id} not found.")

    # ---------------------------------------------------------
    # 2. Get candidate profile
    # ---------------------------------------------------------

    profile = get_profile(user_id)

    if profile is None:
        raise ValueError(f"User {user_id} not found.")

    skills = get_skills(user_id)

    # ---------------------------------------------------------
    # 3. Parse job requirements
    # ---------------------------------------------------------

    required_skills = [
        skill.strip()
        for skill in job["required_skills"].split(",")
        if skill.strip()
    ]

    preferred_skills = [
        skill.strip()
        for skill in job["preferred_skills"].split(",")
        if skill.strip()
    ]

    # ---------------------------------------------------------
    # 4. Retrieve candidate knowledge
    # ---------------------------------------------------------

    knowledge = retrieve_knowledge(
        query=(
            f"Candidate skills, projects, experience and education "
            f"relevant to {job['title']}. "
            f"Required skills: {job['required_skills']}. "
            f"Preferred skills: {job['preferred_skills']}."
        ),
        user_id=user_id,
        limit=6,
    )

    # ---------------------------------------------------------
    # 5. Deterministic skill assessment
    # ---------------------------------------------------------

    deterministic_required = []
    deterministic_preferred = []

    all_required_gaps = []

    for skill in required_skills:

        matches = find_skill_evidence(
            skill=skill,
            knowledge=knowledge,
        )

        if matches:

            status = "strong_evidence"

            evidence = (
                f"Explicit evidence found in "
                f"{len(matches)} candidate knowledge chunk(s)."
            )

        else:

            status = "missing"

            evidence = (
                "No explicit evidence for this skill was found "
                "in the retrieved candidate knowledge."
            )

            all_required_gaps.append(skill)

        deterministic_required.append(
            {
                "skill": skill,
                "status": status,
                "evidence": evidence,
            }
        )

    for skill in preferred_skills:

        matches = find_skill_evidence(
            skill=skill,
            knowledge=knowledge,
        )

        if matches:

            status = "strong_evidence"

            evidence = (
                f"Explicit evidence found in "
                f"{len(matches)} candidate knowledge chunk(s)."
            )

        else:

            status = "missing"

            evidence = (
                "No explicit evidence for this skill was found "
                "in the retrieved candidate knowledge."
            )

        deterministic_preferred.append(
            {
                "skill": skill,
                "status": status,
                "evidence": evidence,
            }
        )

    # ---------------------------------------------------------
    # 6. Deterministic education / experience facts
    # ---------------------------------------------------------

    other_requirements = []

    education = profile.get("education")
    experience = profile.get("experience")

    if education:
        education_status = "supported"
        education_evidence = str(education)
    else:
        education_status = "unknown"
        education_evidence = "No education information available."

    other_requirements.append(
        {
            "requirement": job["education_required"],
            "status": education_status,
            "evidence": education_evidence,
        }
    )

    if experience:
        experience_status = "supported"
        experience_evidence = str(experience)
    else:
        experience_status = "unknown"
        experience_evidence = "No experience information available."

    other_requirements.append(
        {
            "requirement": job["experience_required"],
            "status": experience_status,
            "evidence": experience_evidence,
        }
    )

    # ---------------------------------------------------------
    # 7. Facts sent to Qwen
    # ---------------------------------------------------------
    #
    # IMPORTANT:
    # We deliberately do NOT send all RAG chunks here.
    # The deterministic layer has already extracted the facts.
    #

    facts = {
        "job_title": job["title"],
        "company": job["company"],
        "required_skills": deterministic_required,
        "preferred_skills": deterministic_preferred,
        "other_requirements": other_requirements,
        "skill_gaps": all_required_gaps,
    }

    # ---------------------------------------------------------
    # 8. Small Qwen reasoning request
    # ---------------------------------------------------------

    prompt = f"""
Explain the following job-match facts.

FACTS:
{json.dumps(facts, indent=2)}

Return JSON with exactly:

{{
    "overall_assessment": "one short factual sentence",

    "required_skills": [
        {{
            "skill": "skill name",
            "status": "strong_evidence | partial_evidence | missing | conflicting | unknown",
            "evidence": "short explanation"
        }}
    ],

    "preferred_skills": [
        {{
            "skill": "skill name",
            "status": "strong_evidence | partial_evidence | missing | conflicting | unknown",
            "evidence": "short explanation"
        }}
    ],

    "other_requirements": [
        {{
            "requirement": "requirement",
            "status": "supported | unsupported | unknown",
            "evidence": "short explanation"
        }}
    ],

    "skill_gaps": [
        "skill name"
    ],

    "evidence_summary": [
        "short factual statement"
    ]
}}

IMPORTANT:

Do not change any skill status supplied in FACTS.

Return JSON only.
"""

    response = qwen_model.generate(
        prompt=prompt,
        system_prompt=MATCH_SYSTEM_PROMPT,
    )

    # ---------------------------------------------------------
    # 9. Validate LLM response
    # ---------------------------------------------------------

    try:

        parsed_response = json.loads(response)

        analysis = JobMatchAnalysis.model_validate(
            parsed_response
        )

    except Exception as error:

        raise ValueError(
            f"Invalid job match response from LLM: {error}"
        )

    # ---------------------------------------------------------
    # 10. Return complete result
    # ---------------------------------------------------------

    return {
        "job": job,
        "analysis": analysis.model_dump(),
        "evidence": knowledge,
        "deterministic_assessments": facts,
    }