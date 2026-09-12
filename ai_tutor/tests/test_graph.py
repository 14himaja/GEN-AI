"""
Unit Tests for LangGraph AI Personal Tutor (Standard Library unittest).
=======================================================================
Validates:
1. Graph compilation with MemorySaver.
2. Initial assessment and planning.
3. Human-in-the-loop interrupt on plan review.
4. Resuming with Command(resume=...).
5. Parallel execution & reducer aggregation into parallel_checks.
6. Quiz Subgraph execution.
7. Revision loop execution on low quiz score.
8. State persistence across graph invocations using thread_id.
"""

import os
import sys
import unittest

# Ensure project root is in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from langgraph.types import Command
from ai_tutor.core.graph import build_ai_tutor_graph


class TestAITutorGraph(unittest.TestCase):
    """Test full tutor lifecycle including plan review, parallel checks, and quiz."""

    def test_full_workflow_and_interrupts(self):
        app = build_ai_tutor_graph()
        thread_id = "test-session-001"
        config = {"configurable": {"thread_id": thread_id}}
        
        # 1. Start session with student profile
        student = {
            "name": "Himaja",
            "subject": "DBMS",
            "goal": "Prepare for semester exam",
            "level": "Beginner",
            "available_time": "2 hours/day",
            "topics": ["Normalization"]  # Single topic for quick full-cycle test
        }
        
        initial_input = {
            "student": student,
            "completed_topics": [],
            "parallel_checks": [],
            "quiz_history": [],
            "max_quiz_attempts": 2
        }
        
        # Run until first interrupt (human approval of learning plan)
        for _ in app.stream(initial_input, config):
            pass
            
        state = app.get_state(config)
        self.assertGreater(len(state.tasks), 0)
        self.assertGreater(len(state.tasks[0].interrupts), 0)
        interrupt_val = state.tasks[0].interrupts[0].value
        self.assertEqual(interrupt_val["action"], "review_learning_plan")
        self.assertTrue(any("Normalization" in t for t in interrupt_val["plan"]))
        
        # 2. Resume with plan approval
        resume_cmd = Command(resume={"approved": True})
        for _ in app.stream(resume_cmd, config):
            pass
            
        # State should now be paused at the quiz interrupt
        state = app.get_state(config)
        self.assertGreater(len(state.tasks), 0)
        self.assertGreater(len(state.tasks[0].interrupts), 0)
        quiz_interrupt = state.tasks[0].interrupts[0].value
        self.assertEqual(quiz_interrupt["action"], "take_quiz")
        self.assertEqual(quiz_interrupt["topic"], "Normalization")
        
        # Check that parallel checks executed and reducer aggregated results!
        parallel_checks = state.values.get("parallel_checks", [])
        self.assertEqual(len(parallel_checks), 3)
        self.assertTrue(any("Concept Check" in c for c in parallel_checks))
        self.assertTrue(any("Example Check" in c for c in parallel_checks))
        self.assertTrue(any("Exam Check" in c for c in parallel_checks))
        
        # 3. Simulate low score to verify Adaptive Revision Loop
        # Submit incorrect answers: [0, 0] (Correct are [1, 1])
        resume_low_quiz = Command(resume={"answers": [0, 0]})
        for _ in app.stream(resume_low_quiz, config):
            pass
            
        state = app.get_state(config)
        # Graph should have hit evaluation, triggered revision, and looped back to quiz interrupt!
        self.assertGreater(len(state.tasks), 0)
        self.assertGreater(len(state.tasks[0].interrupts), 0)
        revision_quiz_interrupt = state.tasks[0].interrupts[0].value
        self.assertEqual(revision_quiz_interrupt["action"], "take_quiz")
        self.assertTrue(revision_quiz_interrupt["is_revision"])
        
        # 4. Now answer correctly on revision to PASS and reach Final Assessment!
        # Correct revision answers: [0, 3]
        resume_pass_quiz = Command(resume={"answers": [0, 3]})
        for _ in app.stream(resume_pass_quiz, config):
            pass
            
        state = app.get_state(config)
        # Check that final report was generated
        final_report = state.values.get("final_report")
        self.assertIsNotNone(final_report)
        self.assertEqual(final_report["student_name"], "Himaja")
        self.assertTrue(any("Normalization" in t for t in final_report["topics_completed"]))
        self.assertEqual(final_report["total_quiz_attempts"], 2)


if __name__ == "__main__":
    unittest.main()
