# AI Career Assistant

Intelligent resume parsing, 5-role compatibility scoring, RAG-based job recommendation, and **direct custom Job Description (JD) comparison**.

## 🚀 Key Highlights
- **Two Analysis Modes**:
  1. **Standard 5-Role Track**: Evaluates compatibility across 5 roles (AI/ML, Full Stack, Data Eng, DevOps, Backend) and recommends Top 3 jobs from the indexed mock database using FAISS Vector RAG.
  2. **Custom JD Comparison**: User pastes any specific Job Description to get an exact match percentage, semantic vector similarity score, matched skills, missing skills, candidate strengths, and actionable improvement recommendations.
- **Google Gemini Embeddings**: Powered by `models/gemini-embedding-001` (3072 dimensions) for high-precision semantic representation.
- **Gemini LLM Reasoning**: Structured entity extraction and deep gap evaluation via `models/gemini-2.5-flash`.
- **FAISS Vector DB**: Local in-memory index for fast similarity matching.
- **Glassmorphic UI**: Interactive tabs, drag-and-drop resume upload, and visual scorecards.

---

## 🛠️ Tech Stack
- **Backend**: FastAPI, Uvicorn
- **Orchestration**: LangChain, LangChain-Google-GenAI
- **Vector DB**: FAISS (faiss-cpu)
- **Embedding Model**: Google Gemini (`models/gemini-embedding-001`)
- **LLM**: Google Gemini (`models/gemini-2.5-flash`)
- **Frontend**: Vanilla HTML5, CSS3, Modern JavaScript

---

## ⚙️ Setup & Run

### 1. Configure Environment Variables
Ensure `.env` contains your key:
```ini
GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Run the FastAPI Server
```powershell
.\venv\Scripts\uvicorn main:app --reload --port 8000
```

### 3. Open in Browser
Visit: `http://localhost:8000`

---

## 📋 Features Overview

### Mode 1: 5-Role Track & Top 3 Jobs
1. Upload resume (PDF / DOCX).
2. Get instant match percentages and rationales for:
   - AI / ML Engineer
   - Full Stack Developer
   - Data Engineer
   - DevOps / Cloud Engineer
   - Backend Developer
3. Browse the **Top 3 Recommended Jobs** matched from 20 curated mock postings.

### Mode 2: Custom JD Comparison
1. Switch to the **Custom JD Comparison** tab.
2. Upload your resume and paste any target job description.
3. Review:
   - **Blended Overall Match Score** (combining LLM reasoning + Gemini vector similarity).
   - **Matched Skills** vs **Missing Skills** breakdown.
   - **Key Strengths** for the specific role.
   - **Actionable Recommendations** to boost your interview chances.
