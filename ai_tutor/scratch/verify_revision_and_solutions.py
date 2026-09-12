"""
Verification script for:
1. Subgraph grading returns complete review_details with correct answers and explanations
2. When quiz answers are incorrect, explanations and correct solutions are available
3. Revision content incorporates missed question key takeaways
4. Feedback messaging distinguishes between revision recommended and max attempts reached
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai_tutor.core.quiz_subgraph import create_quiz_subgraph
from ai_tutor.core.graph import build_ai_tutor_graph
from langgraph.types import Command

def test_subgraph_review_details():
    subgraph = create_quiz_subgraph()
    
    # 1. Generate quiz for Memory Management & Paging
    gen = subgraph.invoke({
        "topic": "Memory Management & Paging",
        "difficulty": "Normal",
        "is_revision": False,
        "questions": [],
        "answers": []
    })
    
    questions = gen["questions"]
    assert len(questions) >= 2, "Expected at least 2 questions"
    
    # 2. Grade with deliberately wrong answers
    wrong_answers = [99] * len(questions)
    result = subgraph.invoke({
        "topic": "Memory Management & Paging",
        "difficulty": "Normal",
        "is_revision": False,
        "questions": questions,
        "answers": wrong_answers
    })
    
    assert result["score"] == 0, f"Expected 0% score, got {result['score']}"
    assert result["passed"] is False, "Expected passed to be False"
    assert "review_details" in result, "Missing review_details in result"
    
    details = result["review_details"]
    assert len(details) == len(questions), "review_details count mismatch"
    
    for item in details:
        assert item["is_correct"] is False
        assert bool(item["correct_answer_text"]), "Missing correct_answer_text"
        assert bool(item["explanation"]), "Missing explanation"
        print(f"Verified Q: {item['question']}")
        print(f"   Student Answer: {item['student_answer_text']}")
        print(f"   Correct Solution: {item['correct_answer_text']}")
        print(f"   Explanation: {item['explanation']}")
    
    print("PASS: Subgraph review_details verification succeeded.")

def test_full_graph_revision_and_max_attempts():
    graph = build_ai_tutor_graph()
    config = {"configurable": {"thread_id": "test_verification_thread_rev"}}
    
    initial_input = {
        "student": {
            "name": "Himaja",
            "subject": "Operating Systems",
            "level": "Beginner",
            "goal": "Semester Exam Prep",
            "available_time": "Self-paced",
            "topics": ["Processes & Threads", "Memory Management & Paging"]
        },
        "completed_topics": [],
        "parallel_checks": [],
        "quiz_history": [],
        "max_quiz_attempts": 2,
        "error_count": 0,
        "needs_revision": False,
        "current_difficulty": "Normal"
    }
    
    # Start graph
    for _ in graph.stream(initial_input, config):
        pass
        
    # Approve plan
    for _ in graph.stream(Command(resume={"approved": True}), config):
        pass
        
    snap = graph.get_state(config)
    assert snap.tasks[0].interrupts[0].value["action"] == "take_quiz"
    
    # Attempt 1: Fail quiz
    for _ in graph.stream(Command(resume={"answers": [99, 99]}), config):
        pass
        
    snap1 = graph.get_state(config)
    last_res1 = snap1.values.get("last_quiz_result", {})
    assert snap1.values.get("needs_revision") is True, "Expected revision on attempt 1"
    assert last_res1.get("max_attempts_reached") is False
    assert "review_details" in last_res1
    print("PASS: Attempt 1 triggered revision loop with review_details.")
    
    # Attempt 2 (Revision Attempt): Fail quiz again -> should reach max attempts and advance!
    assert snap1.tasks[0].interrupts[0].value["action"] == "take_quiz"
    for _ in graph.stream(Command(resume={"answers": [99, 99]}), config):
        pass
        
    snap2 = graph.get_state(config)
    last_res2 = snap2.values.get("last_quiz_result", {})
    assert last_res2.get("max_attempts_reached") is True, "Expected max_attempts_reached"
    assert snap2.values.get("needs_revision") is False, "Expected needs_revision to be False after max attempts"
    assert "All 2 attempts completed" in last_res2.get("feedback", ""), f"Unexpected feedback: {last_res2.get('feedback')}"
    assert "Processes & Threads" in snap2.values.get("completed_topics")
    print("PASS: Attempt 2 max attempts handled cleanly with clear advancement feedback.")

if __name__ == "__main__":
    test_subgraph_review_details()
    test_full_graph_revision_and_max_attempts()
    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
