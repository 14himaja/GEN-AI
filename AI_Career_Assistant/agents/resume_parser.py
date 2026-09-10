"""
Resume Parser Agent — Built using LangChain (CampusX Tutorial Concepts)

CampusX Concepts Used:
- ChatGoogleGenerativeAI (Video 3: LangChain Models)
- PromptTemplate (Video 4: Prompts in LangChain)
- Pydantic BaseModel (Video 5: Structured Output in LangChain)
- JsonOutputParser (Video 6: Output Parsers in LangChain)
- LCEL Chain: prompt | llm | output_parser (Video 7: Chains in LangChain)
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_helper import get_chat_model

# -----------------------------------------------------------------
# 1. Output Schema using Pydantic (CampusX Video 5)
# -----------------------------------------------------------------
class CandidateProfile(BaseModel):
    candidate_name: str = Field(description="Full name of candidate from resume")
    email: str = Field(default="Not provided", description="Email address")
    phone: str = Field(default="Not provided", description="Phone number")
    total_experience_years: float = Field(default=0.0, description="Total years of work experience")
    skills: List[str] = Field(description="List of technical and professional skills")
    education: List[str] = Field(default_factory=list, description="Degrees or institutions")
    summary: str = Field(description="2-sentence executive summary of the candidate")

# -----------------------------------------------------------------
# 2. Built-in JSON Output Parser (CampusX Video 6)
# -----------------------------------------------------------------
output_parser = JsonOutputParser(pydantic_object=CandidateProfile)

# -----------------------------------------------------------------
# 3. Prompt Template (CampusX Video 4)
# -----------------------------------------------------------------
prompt = PromptTemplate(
    template="""You are an expert HR Resume Parser.
Carefully read the candidate's resume below and extract their exact details.

Resume Content:
{resume_text}

{format_instructions}
""",
    input_variables=["resume_text"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

# -----------------------------------------------------------------
# 4. LCEL Chain: prompt | llm | output_parser (CampusX Video 7)
# -----------------------------------------------------------------
llm = get_chat_model(temperature=0.1)
parser_chain = prompt | llm | output_parser

def parse_resume(raw_text: str) -> dict:
    """
    Parses candidate resume text into structured JSON using LangChain.
    """
    return parser_chain.invoke({"resume_text": raw_text[:4000]})
