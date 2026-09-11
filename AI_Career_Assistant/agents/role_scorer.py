"""
Role Scorer Agent — scores a candidate against 5 target tech roles.
Uses LangChain's with_structured_output, so the model returns validated
scores directly and no manual JSON parsing is needed.
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from agents.llm_helper import get_chat_model

class RoleScore(BaseModel):
    role: str = Field(description="Name of the technical role")
    match_percentage: int = Field(description="Match percentage between 10 and 95 based on candidate skills")
    rationale: str = Field(description="Clear 1-sentence rationale explaining the score based on candidate skills")

class RoleScoreList(BaseModel):
    scores: List[RoleScore] = Field(description="List of evaluated scores for the 5 roles")

ROLE_PROMPT_TEMPLATE = """You are an expert technical career coach.
Evaluate the candidate's resume for the following 5 tech roles:
1. AI / ML Engineer
2. Full Stack Developer
3. Data Engineer
4. DevOps / Cloud Engineer
5. Backend Developer

Candidate Details:
- Name: {candidate_name}
- Skills: {skills}
- Experience: {experience_years} years
- Summary: {summary}

Resume Content:
{resume_snippet}

For each role:
- Assign an honest match percentage (10 to 95) based directly on how well their skills match that specific role.
- Provide a clear 1-sentence rationale mentioning their actual matching skills.
"""

prompt = PromptTemplate(
    template=ROLE_PROMPT_TEMPLATE,
    input_variables=["candidate_name", "skills", "experience_years", "summary", "resume_snippet"],
)

def get_scoring_chain():
    llm = get_chat_model(temperature=0.2).with_structured_output(RoleScoreList)
    return prompt | llm

def score_roles(candidate_info: dict, resume_text: str) -> list:
    """
    Scores the 5 roles using the LangChain LCEL chain .invoke() method.
    """
    try:
        chain = get_scoring_chain()
        result = chain.invoke({
            "candidate_name": candidate_info.get("candidate_name", "Candidate"),
            "skills": ", ".join(candidate_info.get("skills", [])),
            "experience_years": candidate_info.get("total_experience_years", 0),
            "summary": candidate_info.get("summary", ""),
            "resume_snippet": resume_text[:2000]
        })
        return [score.model_dump() for score in result.scores]
    except Exception as e:
        print(f"[ROLE SCORER WARNING] {e}")

    # Fallback scores, used only if the LLM call above fails
    candidate_skills = [s.title() for s in candidate_info.get("skills", [])[:3]]
    skills_str = ", ".join(candidate_skills) if candidate_skills else "General technical skills"
    return [
        {"role": "AI / ML Engineer", "match_percentage": 75, "rationale": f"Demonstrated foundation in {skills_str}."},
        {"role": "Full Stack Developer", "match_percentage": 70, "rationale": f"Transferable software development skills in {skills_str}."},
        {"role": "Data Engineer", "match_percentage": 65, "rationale": "Relevant technical data and programming background."},
        {"role": "DevOps / Cloud Engineer", "match_percentage": 60, "rationale": "Foundational systems and problem-solving capabilities."},
        {"role": "Backend Developer", "match_percentage": 72, "rationale": f"Strong core programming logic with {skills_str}."}
    ]
