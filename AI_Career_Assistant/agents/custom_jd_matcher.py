"""
Custom JD Matcher Agent — compares a resume against a user-supplied job
description using FAISS semantic similarity plus an LLM structured analysis.
"""

import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from agents.llm_helper import get_chat_model

load_dotenv()

class CustomJDAnalysis(BaseModel):
    match_percentage: int = Field(description="Match score between 10 and 98 based on skills and requirements")
    matched_skills: List[str] = Field(description="Skills present in both candidate profile and the JD")
    missing_skills: List[str] = Field(description="Skills required by the JD that the candidate lacks")
    strengths: List[str] = Field(description="2-3 specific bullet points highlighting candidate strengths")
    gaps_and_recommendations: List[str] = Field(description="2-3 actionable recommendations to improve candidacy")
    executive_verdict: str = Field(description="1-2 sentence overall summary of fit")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

CUSTOM_JD_PROMPT = """You are a senior technical hiring manager.
Compare the candidate's resume against the Target Job Description below.

Target Job Description:
{jd_text}

Candidate Profile:
- Candidate Name: {candidate_name}
- Candidate Skills: {skills}
- Experience: {experience_years} years
- Summary: {summary}

Resume Content:
{resume_snippet}

Evaluate:
1. matched_skills: Extract the real skills from the candidate that match the JD.
2. missing_skills: List key skills from the JD that the candidate lacks.
3. match_percentage: Honest percentage (15 to 98) based on skill coverage.
4. strengths: 2-3 specific bullet points.
5. gaps_and_recommendations: 2-3 actionable recommendations.
6. executive_verdict: Concise 1-2 sentence verdict.
"""

prompt = PromptTemplate(
    template=CUSTOM_JD_PROMPT,
    input_variables=["jd_text", "candidate_name", "skills", "experience_years", "summary", "resume_snippet"],
)

def get_custom_jd_chain():
    llm = get_chat_model(temperature=0.2).with_structured_output(CustomJDAnalysis)
    return prompt | llm

def compare_resume_with_custom_jd(candidate_info: dict, resume_text: str, custom_jd_text: str) -> dict:
    """Compares a resume against a custom JD using FAISS similarity + an LLM analysis chain."""
    # FAISS semantic similarity between resume and JD
    vector_score = 75
    try:
        jd_doc = Document(page_content=custom_jd_text[:2000], metadata={"source": "custom_jd"})
        single_doc_store = FAISS.from_documents([jd_doc], embeddings)
        
        query = f"Skills: {', '.join(candidate_info.get('skills', []))}\nSummary: {candidate_info.get('summary', '')}"
        search_results = single_doc_store.similarity_search_with_score(query, k=1)
        if search_results:
            _, l2_distance = search_results[0]
            # FAISS L2 distance (~0.3 close to ~1.8 far) converted to a 0-100 score
            vector_score = max(30, min(95, int(100 - (l2_distance * 28))))
    except Exception as e:
        print(f"[FAISS VECTOR WARNING] {e}")

    try:
        chain = get_custom_jd_chain()
        analysis = chain.invoke({
            "jd_text": custom_jd_text[:2500],
            "candidate_name": candidate_info.get("candidate_name", "Candidate"),
            "skills": ", ".join(candidate_info.get("skills", [])),
            "experience_years": candidate_info.get("total_experience_years", 0),
            "summary": candidate_info.get("summary", ""),
            "resume_snippet": resume_text[:2000]
        }).model_dump()

        # Blend LLM judgment with FAISS semantic similarity for the final score
        llm_score = analysis.get("match_percentage", 70)
        final_score = int(0.65 * llm_score + 0.35 * vector_score)
        analysis["match_percentage"] = final_score
        analysis["semantic_similarity_score"] = vector_score
        return analysis

    except Exception as e:
        print(f"[CUSTOM JD LLM WARNING] {e}")
        # Fallback analysis, used only if the LLM call above fails
        cand_name = candidate_info.get("candidate_name", "Candidate")
        cand_skills = candidate_info.get("skills", ["General Software Engineering"])
        return {
            "match_percentage": vector_score,
            "semantic_similarity_score": vector_score,
            "matched_skills": cand_skills[:4],
            "missing_skills": ["Specialized domain requirements from JD"],
            "strengths": [
                f"Solid technical foundation demonstrated in {', '.join(cand_skills[:3])}.",
                "Relevant experience applicable to core role responsibilities."
            ],
            "gaps_and_recommendations": [
                "Tailor resume summary to directly mirror required keywords from the JD.",
                "Highlight quantifiable metrics for relevant past projects."
            ],
            "executive_verdict": f"{cand_name} demonstrates strong potential with a {vector_score}% semantic alignment to this role."
        }
