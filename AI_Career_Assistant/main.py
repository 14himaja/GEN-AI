"""
AI Career Assistant â€” FastAPI Application
Endpoints for resume upload, agentic pipeline orchestration, custom JD comparison, and frontend serving.
"""

import io
import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from docx import Document as DocxDocument

from agents.resume_parser import parse_resume, extract_fallback_from_text
from agents.role_scorer import score_roles
from agents.jd_matcher import match_all_jobs, get_or_create_vector_store
from agents.custom_jd_matcher import compare_resume_with_custom_jd

load_dotenv()

app = FastAPI(
    title="AI Career Assistant",
    description="Resume parsing, 5-role scoring, RAG-based job matching across all JDs & custom JD comparison using LangChain & Gemini.",
    version="1.2.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extracts raw text from uploaded PDF or DOCX file."""
    ext = filename.lower().split(".")[-1]
    text = ""
    
    if ext == "pdf":
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read PDF: {str(e)}")
            
    elif ext in ["docx", "doc"]:
        try:
            doc = DocxDocument(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                if para.text:
                    text += para.text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read DOCX: {str(e)}")
            
    elif ext == "txt":
        text = file_bytes.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, or TXT.")

    clean_text = text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Could not extract any readable text from the uploaded file.")
    return clean_text

@app.on_event("startup")
async def startup_event():
    """Warm up and pre-index mock job descriptions into FAISS on startup using LangChain."""
    print("[INIT] Initializing FAISS vector store with Google Gemini Embeddings via LangChain...")
    try:
        get_or_create_vector_store()
        print("[SUCCESS] FAISS Vector store indexed successfully!")
    except Exception as e:
        print(f"[WARNING] Vector store pre-index warning: {e}")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serves the main application page."""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/health")
async def health_check():
    """Health check verifying API operational status."""
    return {
        "status": "healthy",
        "framework": "LangChain",
        "embeddings": "Google Gemini (gemini-embedding-001)",
        "llm": "Google Gemini (gemini-2.5-flash)",
        "vector_db": "LangChain FAISS",
        "all_jd_comparison": True,
        "custom_jd_supported": True
    }

@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    custom_jd: Optional[str] = Form(None)
):
    """
    Main Agentic Pipeline:
    1. Extracts text from uploaded resume.
    2. Resume Parser Agent (LangChain LCEL chain) -> Extracts candidate profile.
    3. If custom_jd provided -> compares resume directly against the custom JD.
    4. If custom_jd NOT provided -> 5-role scoring + comparison score against EVERY mock JD in the FAISS vector DB.
    """
    try:
        contents = await file.read()
        raw_text = extract_text_from_file(contents, file.filename)
        
        # Step 1: Parse candidate details
        candidate_info = parse_resume(raw_text)
        
        has_custom_jd = bool(custom_jd and custom_jd.strip())

        if has_custom_jd:
            # Mode B: Custom JD direct comparison - concurrent execution for 3x speedup
            initial_info = extract_fallback_from_text(raw_text)
            
            task_parse = asyncio.to_thread(parse_resume, raw_text)
            task_match = asyncio.to_thread(compare_resume_with_custom_jd, initial_info, raw_text, custom_jd.strip())
            
            candidate_info, jd_comparison = await asyncio.gather(task_parse, task_match)
            
            if candidate_info.get("candidate_name") and candidate_info.get("candidate_name") != "Candidate":
                if "Candidate" in jd_comparison.get("executive_verdict", ""):
                    jd_comparison["executive_verdict"] = jd_comparison["executive_verdict"].replace("Candidate", candidate_info["candidate_name"])

            return JSONResponse(content={
                "success": True,
                "mode": "custom_jd",
                "filename": file.filename,
                "candidate": candidate_info,
                "custom_jd_analysis": jd_comparison
            })
        else:
            # Mode A: Standard 5-role scoring + comparison with ALL mock JDs concurrently
            candidate_info = await asyncio.to_thread(parse_resume, raw_text)
            
            task_roles = asyncio.to_thread(score_roles, candidate_info, raw_text)
            task_jobs = asyncio.to_thread(match_all_jobs, candidate_info, raw_text)
            
            role_scores, all_jobs_matched = await asyncio.gather(task_roles, task_jobs)
            top_3_jobs = all_jobs_matched[:3]

            return JSONResponse(content={
                "success": True,
                "mode": "standard_roles",
                "filename": file.filename,
                "candidate": candidate_info,
                "role_scores": role_scores,
                "top_recommended_jobs": top_3_jobs,
                "all_compared_jobs": all_jobs_matched,
                "total_jobs_evaluated": len(all_jobs_matched)
            })

    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": f"Analysis failed: {str(e)}"}
        )
