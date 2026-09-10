import os
import sys
sys.path.insert(0, os.path.abspath("."))
from dotenv import load_dotenv
load_dotenv()

from agents.resume_parser import parse_resume
from agents.role_scorer import score_roles
from agents.jd_matcher import match_all_jobs
from agents.custom_jd_matcher import compare_resume_with_custom_jd

with open("test_resume.txt", "r") as f:
    sample_resume = f.read()

print("--- 1. Testing LangChain Resume Parser ---")
candidate = parse_resume(sample_resume)
print("Parsed Candidate Name:", candidate.get("candidate_name"))
print("Parsed Skills Count:", len(candidate.get("skills", [])))
print("Parsed Skills Sample:", candidate.get("skills", [])[:5])

print("\n--- 2. Testing LangChain Role Scorer ---")
scores = score_roles(candidate, sample_resume)
print(f"Roles scored: {len(scores)}")
for s in scores:
    print(f"  {s['role']}: {s['match_percentage']}% - {s['rationale'][:60]}...")

print("\n--- 3. Testing LangChain Job Matcher (FAISS) ---")
jobs = match_all_jobs(candidate, sample_resume)
print(f"Total jobs compared: {len(jobs)}")
print(f"Top 1 match: {jobs[0]['title']} at {jobs[0]['company']} - {jobs[0]['match_score']}%")

print("\n--- 4. Testing LangChain Custom JD Matcher ---")
custom_jd = """Senior Python Developer:
Looking for a Python expert with FastAPI, Docker, SQL, and Microservices experience. 
Must understand RESTful APIs and CI/CD pipelines."""
custom_res = compare_resume_with_custom_jd(candidate, sample_resume, custom_jd)
print("Custom JD Match Percentage:", custom_res.get("match_percentage"), "%")
print("Custom JD Matched Skills:", custom_res.get("matched_skills"))
print("Custom JD Missing Skills:", custom_res.get("missing_skills"))
print("Verdict:", custom_res.get("executive_verdict"))
print("\nALL LANGCHAIN AGENTS TESTED SUCCESSFULLY!")
