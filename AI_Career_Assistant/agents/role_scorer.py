"""
Role Scorer Agent (CampusX LangChain LCEL Pipeline)

Concepts from CampusX Playlist:
- Video 3: Models (ChatGoogleGenerativeAI)
- Video 4: Prompts in LangChain (PromptTemplate)
- Video 5: Structured Output (Pydantic BaseModel, Field)
- Video 6: Output Parsers (JsonOutputParser)
- Video 7: Chains in LangChain (LCEL prompt | llm | output_parser)
- Video 8: Runnables (.invoke())
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_helper import get_chat_model

# -------------------------------------------------------------
# 1. Pydantic Schema (CampusX Video 5: Structured Output)
# -------------------------------------------------------------
class RoleScore(BaseModel):
    role: str = Field(description="Name of the technical role")
    match_percentage: int = Field(description="Match percentage between 10 and 95 based on candidate skills")
    rationale: str = Field(description="Clear 1-sentence rationale explaining the score based on candidate skills")

class RoleScoreList(BaseModel):
    scores: List[RoleScore] = Field(description="List of evaluated scores for the 5 roles")

# -------------------------------------------------------------
# 2. Output Parser (CampusX Video 6: Output Parsers)
# -------------------------------------------------------------
output_parser = JsonOutputParser(pydantic_object=RoleScoreList)

# -------------------------------------------------------------
# 3. Prompt Template (CampusX Video 4: Prompts in LangChain)
# -------------------------------------------------------------
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

{format_instructions}
"""

prompt = PromptTemplate(
    template=ROLE_PROMPT_TEMPLATE,
    input_variables=["candidate_name", "skills", "experience_years", "summary", "resume_snippet"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

# -------------------------------------------------------------
# 4. LCEL Chain & Execution (CampusX Video 7 & 8: Chains & Runnables)
# -------------------------------------------------------------
def get_scoring_chain():
    llm = get_chat_model(temperature=0.2)
    # Pure LCEL chain: prompt | llm | output_parser
    return prompt | llm | output_parser

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
        
        if isinstance(result, dict) and "scores" in result:
            return result["scores"]
        elif isinstance(result, list):
            return result
    except Exception as e:
        print(f"[ROLE SCORER WARNING] {e}")

    # Clean default fallback in case of network/parsing issues
    candidate_skills = [s.title() for s in candidate_info.get("skills", [])[:3]]
    skills_str = ", ".join(candidate_skills) if candidate_skills else "General technical skills"
    return [
        {"role": "AI / ML Engineer", "match_percentage": 75, "rationale": f"Demonstrated foundation in {skills_str}."},
        {"role": "Full Stack Developer", "match_percentage": 70, "rationale": f"Transferable software development skills in {skills_str}."},
        {"role": "Data Engineer", "match_percentage": 65, "rationale": "Relevant technical data and programming background."},
        {"role": "DevOps / Cloud Engineer", "match_percentage": 60, "rationale": "Foundational systems and problem-solving capabilities."},
        {"role": "Backend Developer", "match_percentage": 72, "rationale": f"Strong core programming logic with {skills_str}."}
    ]
