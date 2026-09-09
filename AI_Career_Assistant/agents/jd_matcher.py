"""
Job Description Matcher Agent (RAG Pipeline using purely LangChain built-ins)
Uses:
- LangChain GoogleGenerativeAIEmbeddings (models/gemini-embedding-001)
- LangChain FAISS vector store
- In-built similarity_search_with_relevance_scores (no custom cosine math from scratch)
- In-built Document abstraction & metadata
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from data.job_descriptions import MOCK_JOB_DESCRIPTIONS

load_dotenv()

# LangChain Gemini Embeddings wrapper
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# In-memory FAISS vector store singleton
vector_store: FAISS = None

def get_or_create_vector_store() -> FAISS:
    """
    Builds the FAISS vector store using LangChain's Document abstraction.
    Embeds each mock job description and stores metadata for retrieval.
    """
    global vector_store
    if vector_store is not None:
        return vector_store

    # Convert mock JDs to LangChain Document objects
    documents = []
    for jd in MOCK_JOB_DESCRIPTIONS:
        page_content = (
            f"Job Title: {jd['title']}\n"
            f"Category: {jd['role_category']}\n"
            f"Company: {jd['company']}\n"
            f"Location: {jd['location']}\n"
            f"Required Skills: {', '.join(jd['skills'])}\n"
            f"Job Overview: {jd['description']}"
        )
        metadata = {
            "id": jd["id"],
            "title": jd["title"],
            "company": jd["company"],
            "role_category": jd["role_category"],
            "location": jd["location"],
            "skills": jd["skills"],
            "description": jd["description"]
        }
        documents.append(Document(page_content=page_content, metadata=metadata))

    # Built-in LangChain FAISS factory method
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

def match_all_jobs(candidate_info: dict, resume_text: str) -> List[Dict[str, Any]]:
    """
    Compares the candidate resume against EVERY indexed mock JD using LangChain's
    built-in FAISS vector similarity search with relevance scores.
    Returns comparison scores for all JDs, sorted descending by match percentage.
    """
    db = get_or_create_vector_store()

    # Query string formulated from candidate profile
    query = (
        f"Summary: {candidate_info.get('summary', '')}\n"
        f"Skills: {', '.join(candidate_info.get('skills', []))}\n"
        f"Experience: {resume_text[:1200]}"
    )

    # Use LangChain built-in similarity search with scores
    # k=len(MOCK_JOB_DESCRIPTIONS) ensures EVERY JD is compared and scored
    results_with_scores = db.similarity_search_with_score(query, k=len(MOCK_JOB_DESCRIPTIONS))

    candidate_skills_lower = {s.lower() for s in candidate_info.get("skills", [])}
    all_matched = []

    for rank, (doc, l2_distance) in enumerate(results_with_scores, 1):
        meta = doc.metadata
        jd_skills = meta.get("skills", [])
        
        # Calculate overlapping skills
        overlapping = [
            s for s in jd_skills 
            if s.lower() in candidate_skills_lower or any(s.lower() in cs for cs in candidate_skills_lower)
        ]
        
        # Convert FAISS L2 Euclidean distance to normalized 0-100 percentage
        # Distance ranges ~ 0.3 (close) to 1.8 (far)
        base_match = max(30, min(95, int(100 - (l2_distance * 28))))
        if len(overlapping) >= 2:
            base_match = min(98, base_match + (len(overlapping) * 3))

        all_matched.append({
            "rank": rank,
            "job_id": meta.get("id"),
            "title": meta.get("title"),
            "company": meta.get("company"),
            "location": meta.get("location"),
            "role_category": meta.get("role_category"),
            "match_score": int(base_match),
            "matched_skills": overlapping if overlapping else jd_skills[:2],
            "all_required_skills": jd_skills,
            "description": meta.get("description")
        })

    # Sort descending by match score
    all_matched.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Assign final 1-based ranks
    for idx, item in enumerate(all_matched, 1):
        item["rank"] = idx

    return all_matched
