"""
Role Scorer Agent (LangChain LCEL with Built-in JsonOutputParser)

Beginner-Friendly Explanation:
1. Evaluates candidate fit across 5 core tech roles:
   - AI / ML Engineer
   - Full Stack Developer
   - Data Engineer
   - DevOps / Cloud Engineer
   - Backend Developer
2. Uses LangChain's PromptTemplate and JsonOutputParser with Pydantic.
3. Scores and rationales are directly based on the candidate's actual extracted skills.
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_helper import get_chat_model

# -------------------------------------------------------------
# 1. Define Output Schema
# -------------------------------------------------------------
class RoleScore(BaseModel):
    role: str = Field(description="One of the 5 tech roles")
    match_percentage: int = Field(description="Percentage match score between 10 and 95")
    rationale: str = Field(description="Clear explanation explaining why candidate received this score based on their skills")

class RoleScoreList(BaseModel):
    scores: List[RoleScore] = Field(description="List of 5 evaluated role scores")

# -------------------------------------------------------------
# 2. LangChain Built-in JSON Parser
# -------------------------------------------------------------
output_parser = JsonOutputParser(pydantic_object=RoleScoreList)

# -------------------------------------------------------------
# 3. Prompt Template
# -------------------------------------------------------------
ROLE_SCORING_PROMPT = """You are an expert technical career advisor.
Evaluate the candidate's resume and assign a match percentage (10 to 95) for each of these 5 roles:
1. AI / ML Engineer
2. Full Stack Developer
3. Data Engineer
4. DevOps / Cloud Engineer
5. Backend Developer

Candidate Details:
- Candidate Name: {candidate_name}
- Candidate Skills: {skills}
- Experience: {experience_years} years
- Summary: {summary}

Full Resume Content:
{resume_snippet}

Base the percentage and rationale directly on the skills and experience listed above.

{format_instructions}
"""

prompt = PromptTemplate(
    template=ROLE_SCORING_PROMPT,
    input_variables=["candidate_name", "skills", "experience_years", "summary", "resume_snippet"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

def get_scoring_chain():
    llm = get_chat_model(temperature=0.2)
    return prompt | llm | output_parser

# Keyword definitions for calculating scores based on real skills
ROLE_SKILL_MAP = {
    "AI / ML Engineer": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "nlp", "llms", "langchain", "rag", "pandas", "numpy", "scikit-learn"],
    "Full Stack Developer": ["javascript", "typescript", "react", "html", "css", "node.js", "angular", "vue.js", "next.js", "frontend", "full stack"],
    "Data Engineer": ["sql", "python", "spark", "airflow", "kafka", "data engineering", "etl", "postgresql", "mysql", "mongodb"],
    "DevOps / Cloud Engineer": ["docker", "kubernetes", "aws", "azure", "gcp", "linux", "git", "ci/cd", "devops", "cloud"],
    "Backend Developer": ["python", "fastapi", "django", "flask", "java", "c++", "c#", "rest api", "microservices", "sql", "redis"]
}

def calculate_skills_based_scores(candidate_info: dict) -> list:
    """
    Computes realistic percentage scores based on candidate's actual extracted skills.
    Used if AI response needs a supplement or fallback.
    """
    candidate_skills = [s.lower() for s in candidate_info.get("skills", [])]
    results = []

    for role, keywords in ROLE_SKILL_MAP.items():
        matched = [k for k in keywords if any(k in cs for cs in candidate_skills)]
        # Score calculation: base 35% + 12% per matched keyword, capped at 92%
        pct = min(92, 35 + (len(matched) * 12))
        if matched:
            rationale = f"Matched {len(matched)} key skills: {', '.join(s.title() for s in matched[:4])}."
        else:
            rationale = "Foundational background with potential for cross-training."
        
        results.append({
            "role": role,
            "match_percentage": pct,
            "rationale": rationale
        })

    return results

def score_roles(candidate_info: dict, resume_text: str) -> list:
    """
    Scores the 5 roles using LangChain's LCEL chain.
    """
    try:
        chain = get_scoring_chain()
        parsed_result = chain.invoke({
            "candidate_name": candidate_info.get("candidate_name", "Candidate"),
            "skills": ", ".join(candidate_info.get("skills", [])),
            "experience_years": candidate_info.get("total_experience_years", 0),
            "summary": candidate_info.get("summary", ""),
            "resume_snippet": resume_text[:2500]
        })
        
        if isinstance(parsed_result, dict) and "scores" in parsed_result:
            return parsed_result["scores"]
        elif isinstance(parsed_result, list):
            return parsed_result
        return calculate_skills_based_scores(candidate_info)
    except Exception as e:
        print(f"[SCORING WARNING] Using skill-based score calculation: {e}")
        return calculate_skills_based_scores(candidate_info)
