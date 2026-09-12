import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from langgraph.types import Command
from ai_tutor.core.graph import build_ai_tutor_graph

def run_test():
    print("=== Testing New Interactive Flow ===")
    app = build_ai_tutor_graph()
    thread_id = "test-interactive-42"
    config = {"configurable": {"thread_id": thread_id}}

    # 1. Start session with Python subject
    student = {
        "name": "Himaja",
        "subject": "Python",
        "goal": "Semester Exam Prep",
        "level": "Beginner",
        "available_time": "2 hours/day",
        "topics": []  # Empty so it triggers diagnostic test!
    }

    initial_input = {
        "student": student,
        "completed_topics": [],
        "parallel_checks": [],
        "quiz_history": [],
        "max_quiz_attempts": 2
    }

    # Stream to first interrupt
    for _ in app.stream(initial_input, config):
        pass

    state = app.get_state(config)
    assert len(state.tasks) > 0 and len(state.tasks[0].interrupts) > 0
    interrupt_1 = state.tasks[0].interrupts[0].value
    print("[STEP 1 SUCCESS] Paused at interrupt 1:", interrupt_1["action"])
    assert interrupt_1["action"] == "take_diagnostic_quiz"
    print("  Subject:", interrupt_1["subject"])
    print("  Diagnostic questions count:", len(interrupt_1["questions"]))

    # 2. Answer diagnostic quiz (answer question 1 right, question 2 wrong)
    # Question 1: mutable type -> list (correct=1)
    # Question 2: list comp -> answer wrong (e.g. 2 instead of 0)
    answers = [1, 2, 1, 1, 1]
    resume_diag = Command(resume={"answers": answers})
    for _ in app.stream(resume_diag, config):
        pass

    state = app.get_state(config)
    assert len(state.tasks) > 0 and len(state.tasks[0].interrupts) > 0
    interrupt_2 = state.tasks[0].interrupts[0].value
    print("\n[STEP 2 SUCCESS] Paused at interrupt 2:", interrupt_2["action"])
    assert interrupt_2["action"] == "review_learning_plan"
    print("  Diagnostic Score:", interrupt_2.get("initial_score"), "%")
    print("  Weak Topics:", interrupt_2.get("weak_topics"))
    print("  Strong Topics:", interrupt_2.get("strong_topics"))
    print("  Proposed Plan:", interrupt_2.get("plan"))

    # 3. User customizes the plan (adds a custom topic, removes one)
    custom_plan = [
        "Control Flow & Loops",  # Moved weak topic
        "AsyncIO & Advanced Concurrency",  # Added custom topic!
        "Functions & Scope",
        "Object-Oriented Programming"
    ]
    resume_plan = Command(resume={"approved": True, "modified_plan": custom_plan})
    for _ in app.stream(resume_plan, config):
        pass

    state = app.get_state(config)
    print("\n[STEP 3 SUCCESS] Resumed with modified plan!")
    print("  Active Topic:", state.values.get("current_topic"))
    print("  Current Plan in State:", state.values.get("learning_plan"))
    assert state.values.get("learning_plan") == custom_plan
    assert state.values.get("current_topic") == "Control Flow & Loops"

    print("\nALL INTERACTIVE CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    run_test()
