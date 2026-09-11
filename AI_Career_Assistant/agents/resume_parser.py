"""
Resume Parser Agent — extracts structured candidate data from resume text.
Uses LangChain's with_structured_output, so the model returns validated data
directly and no manual JSON parsing is needed.
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from agents.llm_helper import get_chat_model

class CandidateProfile(BaseModel):
    candidate_name: str = Field(description="Full name of candidate from resume")
    email: str = Field(default="Not provided", description="Email address")
    phone: str = Field(default="Not provided", description="Phone number")
    total_experience_years: float = Field(default=0.0, description="Total years of work experience")
    skills: List[str] = Field(description="List of technical and professional skills")
    education: List[str] = Field(default_factory=list, description="Degrees or institutions")
    summary: str = Field(description="2-sentence executive summary of the candidate")

prompt = PromptTemplate(
    template="""You are an expert HR Resume Parser.
Carefully read the candidate's resume below and extract their exact details.

Resume Content:
{resume_text}
""",
    input_variables=["resume_text"],
)

llm = get_chat_model(temperature=0.1).with_structured_output(CandidateProfile)
parser_chain = prompt | llm

def parse_resume(raw_text: str) -> dict:
    """
    Parses candidate resume text into a structured dict using LangChain.
    """
    result = parser_chain.invoke({"resume_text": raw_text[:4000]})
    return result.model_dump()
