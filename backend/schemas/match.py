from pydantic import BaseModel


class SkillAssessment(BaseModel):
    skill: str
    status: str
    evidence: str


class RequirementAssessment(BaseModel):
    requirement: str
    status: str
    evidence: str


class JobMatchAnalysis(BaseModel):
    overall_assessment: str
    required_skills: list[SkillAssessment]
    preferred_skills: list[SkillAssessment]
    other_requirements: list[RequirementAssessment]
    skill_gaps: list[str]
    evidence_summary: list[str]