# LangChain Concepts Guide — AI Career Assistant

This project is built **strictly using the concepts taught in the CampusX Generative AI using LangChain playlist** (18 videos):
[CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PL8n_RR1gqRmycHk4pYlQPYd2RoqE5fHCF)

No complex custom regex scrapers, no hardcoded keyword databases, and no non-standard libraries. Every module is clean, concise, and beginner-friendly.

---

## 1. Syllabus & Project Mapping

| Playlist Video | Concept Taught | Implementation in Project | File |
|---|---|---|---|
| **Video 1-2** | Introduction & Core Components | Architecture of prompts, models, output parsers, documents, vector stores | Entire repository |
| **Video 3** | Models in LangChain | `ChatGoogleGenerativeAI`, `GoogleGenerativeAIEmbeddings` | [`agents/llm_helper.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/llm_helper.py), [`agents/jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/jd_matcher.py) |
| **Video 4** | Prompts (`PromptTemplate`) | Formats structured prompts with placeholders & partial format instructions | [`agents/resume_parser.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/resume_parser.py), [`agents/role_scorer.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/role_scorer.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 5** | Structured Output (`BaseModel`, `Field`) | Pydantic schemas: `CandidateProfile`, `RoleScoreList`, `CustomJDAnalysis` | [`agents/resume_parser.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/resume_parser.py), [`agents/role_scorer.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/role_scorer.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 6** | Output Parsers (`JsonOutputParser`) | Enforces structured JSON output matching Pydantic models automatically | [`agents/resume_parser.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/resume_parser.py), [`agents/role_scorer.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/role_scorer.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 7** | Chains (LCEL) | LangChain Expression Language pipe operator: `chain = prompt \| llm \| output_parser` | [`agents/resume_parser.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/resume_parser.py), [`agents/role_scorer.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/role_scorer.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 8-9** | Runnables & Invocations | Running chains synchronously & asynchronously via `.invoke({...})` | [`agents/resume_parser.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/resume_parser.py), [`agents/role_scorer.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/role_scorer.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 10** | Document Loaders / Document | `Document(page_content=..., metadata=...)` standard document representation | [`agents/jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/jd_matcher.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 11-12**| Vector Stores (`FAISS`) | `FAISS.from_documents(documents, embeddings)` | [`agents/jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/jd_matcher.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 13** | Retrievers & Similarity Search | In-built `vector_store.similarity_search_with_score(query, k=...)` | [`agents/jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/jd_matcher.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 14-15**| Building a RAG System | Ingests documents, indexes in FAISS, queries semantic matches, and feeds context into prompt | [`agents/jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/jd_matcher.py), [`agents/custom_jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/custom_jd_matcher.py) |
| **Video 16-18**| Tools & Agents (`@tool`) | `@tool def fetch_mock_job_descriptions()` with `.invoke({})` | [`agents/jd_matcher.py`](file:///c:/Users/sreej/OneDrive/Desktop/SYNXA-LEARN/AI_Career_Assistant/agents/jd_matcher.py) |

---

## 2. Beginner-Friendly Code Walkthrough

### A. Resume Parser Agent (`agents/resume_parser.py`)
- **Pydantic Model**: Defines `CandidateProfile` with `candidate_name`, `email`, `skills`, `total_experience_years`, and `summary`.
- **JsonOutputParser**: Injects schema instructions into the prompt automatically: `output_parser.get_format_instructions()`.
- **LCEL Chain**:
  ```python
  chain = prompt | llm | output_parser
  result = chain.invoke({"resume_text": raw_text})
  ```
  That's all! Under 50 lines of clear, readable code.

### B. Role Scorer Agent (`agents/role_scorer.py`)
- Takes the parsed skills and summary.
- Uses `PromptTemplate` and `JsonOutputParser` with Pydantic `RoleScoreList`.
- Prompts the LLM to score the candidate across 5 tech roles (AI/ML, Full Stack, Data Engineer, DevOps, Backend).
- Executed with `.invoke()`.

### C. Job Matcher Agent (`agents/jd_matcher.py`)
- Defines `@tool def fetch_mock_job_descriptions()`.
- Converts each JD into a LangChain `Document(page_content=..., metadata=...)`.
- Indexes all 20 job descriptions into FAISS using `FAISS.from_documents(documents, embeddings)`.
- Uses built-in `similarity_search_with_score(query, k=20)` to rank all 20 job descriptions against the candidate's profile.

### D. Custom JD Matcher Agent (`agents/custom_jd_matcher.py`)
- Converts user-supplied JD into a LangChain `Document`.
- Runs FAISS vector search to compute semantic alignment.
- Runs an LCEL chain (`prompt | llm | output_parser`) to extract matched skills, missing skills, strengths, recommendations, and executive verdict.
- Combines semantic similarity with LLM reasoning.

### E. FastAPI Server (`main.py`)
- Orchestrates the agents cleanly with `asyncio.to_thread` for fast, non-blocking execution.
- Returns clean JSON with percentages for UI consumption.
