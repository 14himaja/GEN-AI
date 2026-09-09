"""
Resume Parser Agent (LangChain LCEL with Built-in JsonOutputParser)

Beginner-Friendly Explanation:
1. Pydantic Schema: Defines what data we want (name, email, skills, etc.).
2. JsonOutputParser: LangChain's built-in tool that forces the AI to output valid JSON.
3. PromptTemplate: The instructions we send to the AI model.
4. LCEL Chain (prompt | llm | output_parser): Runs the prompt, passes to LLM, and parses the JSON.
"""

import re
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_helper import get_chat_model

# -------------------------------------------------------------
# 1. Define the Candidate Profile Schema (What fields we need)
# -------------------------------------------------------------
class CandidateProfile(BaseModel):
    candidate_name: str = Field(default="Candidate", description="Full Name of the candidate")
    email: str = Field(default="Not provided", description="Email address found in resume")
    phone: str = Field(default="Not provided", description="Phone number found in resume")
    total_experience_years: float = Field(default=0.0, description="Total years of work experience")
    skills: List[str] = Field(default_factory=list, description="List of technical and professional skills")
    education: List[str] = Field(default_factory=list, description="Degrees, universities, or qualifications")
    summary: str = Field(default="", description="2-sentence summary of the candidate's background")

# -------------------------------------------------------------
# 2. LangChain Built-in JSON Output Parser
# -------------------------------------------------------------
output_parser = JsonOutputParser(pydantic_object=CandidateProfile)

# -------------------------------------------------------------
# 3. Prompt Template
# -------------------------------------------------------------
PARSER_PROMPT = """You are an expert HR Resume Parser.
Carefully read the candidate's resume text below and extract their exact details.

Resume Content:
{resume_text}

{format_instructions}
"""

prompt = PromptTemplate(
    template=PARSER_PROMPT,
    input_variables=["resume_text"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

# -------------------------------------------------------------
# 4. LangChain LCEL Chain: prompt | llm | output_parser
# -------------------------------------------------------------
def get_parser_chain():
    llm = get_chat_model(temperature=0.1)
    return prompt | llm | output_parser

# Common tech skills dictionary for fallback extraction
KNOWN_SKILLS = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "HTML", "CSS", "SQL",
    "FastAPI", "Flask", "Django", "React", "Node.js", "Angular", "Vue.js", "Next.js",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "Git", "CI/CD",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-Learn",
    "Natural Language Processing", "NLP", "Computer Vision", "LLMs", "LangChain", "RAG",
    "Pandas", "NumPy", "Apache Spark", "Airflow", "Kafka", "Data Engineering",
    "Tableau", "Power BI", "Data Analysis", "REST API", "Microservices", "Problem Solving"
]

def extract_fallback_from_text(raw_text: str) -> dict:
    """
    Fallback parser: Extracts real details directly from the uploaded resume text
    if the AI model is temporarily unreachable or rate-limited.
    """
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    # 1. Candidate Name (usually the first non-empty line)
    name = "Candidate"
    for line in lines[:5]:
        # Avoid lines that look like headers or contact info
        if "@" not in line and "resume" not in line.lower() and "curriculum" not in line.lower() and len(line.split()) <= 4:
            name = line
            break

    # 2. Email extraction
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
    email = email_match.group(0) if email_match else "Not provided"

    # 3. Phone extraction
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", raw_text)
    phone = phone_match.group(0) if phone_match else "Not provided"

    # 4. Skills extraction by scanning for known keywords in resume text
    found_skills = []
    text_lower = raw_text.lower()
    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    if not found_skills:
        found_skills = ["Software Engineering", "Problem Solving"]

    # 5. Experience estimate
    exp_match = re.search(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)", text_lower)
    exp_years = float(exp_match.group(1)) if exp_match else 1.0

    return {
        "candidate_name": name,
        "email": email,
        "phone": phone,
        "total_experience_years": exp_years,
        "skills": found_skills[:12],
        "education": ["Extracted from resume"],
        "summary": f"{name} is a software professional with demonstrated experience in {', '.join(found_skills[:4])}."
    }

def parse_resume(raw_text: str) -> dict:
    """
    Parses resume text using LangChain's built-in JsonOutputParser.
    Returns a clean Python dictionary with real candidate details.
    """
    try:
        chain = get_parser_chain()
        result = chain.invoke({"resume_text": raw_text[:4000]})
        
        # Ensure candidate name isn't empty or default if text has content
        if not result.get("candidate_name") or result.get("candidate_name").lower() == "candidate":
            fallback = extract_fallback_from_text(raw_text)
            result["candidate_name"] = fallback["candidate_name"]
            if not result.get("skills"):
                result["skills"] = fallback["skills"]
        return result
    except Exception as e:
        print(f"[PARSER WARNING] Using text extraction fallback: {e}")
        return extract_fallback_from_text(raw_text)
