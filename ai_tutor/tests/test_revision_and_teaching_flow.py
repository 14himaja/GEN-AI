"""
Verification script for:
1. Teaching explanation comes before quiz
2. Pass quiz -> advance to next topic
3. Fail quiz -> enter revision loop for same topic with simplified explanation
4. Verification of all expanded subjects (14 subjects)
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai_tutor.core.graph import build_ai_tutor_graph
from langgraph.types import Command
from ai_tutor.core.knowledge import (
    DEFAULT_SUBJECT_TOPICS,
    INITIAL_ASSESSMENT_DB,
    get_initial_questions,
    get_default_topics_for_subject,
    get_teaching_material
)


class TestRevisionAndExpandedSubjects(unittest.TestCase):

    def test_all_14_subjects_available(self):
        expected_subjects = [
            "DBMS", "PYTHON", "OPERATING SYSTEMS", "MACHINE LEARNING",
            "DATA STRUCTURES & ALGORITHMS", "WEB DEVELOPMENT", "COMPUTER NETWORKS",
            "CLOUD COMPUTING", "CYBERSECURITY", "SYSTEM DESIGN", "DEVOPS",
            "OBJECT-ORIENTED PROGRAMMING", "GENERATIVE AI", "DATA SCIENCE"
        ]
        for subj in expected_subjects:
            self.assertIn(subj, DEFAULT_SUBJECT_TOPICS, f"Missing {subj} in DEFAULT_SUBJECT_TOPICS")
            self.assertIn(subj, INITIAL_ASSESSMENT_DB, f"Missing {subj} in INITIAL_ASSESSMENT_DB")
            
            topics = get_default_topics_for_subject(subj)
            self.assertTrue(len(topics) >= 5, f"{subj} has fewer than 5 topics")
            
            questions = get_initial_questions(subj)
            self.assertTrue(len(questions) >= 3, f"{subj} has fewer than 3 diagnostic questions")
            
            # Check teaching material for first topic
            mat = get_teaching_material(topics[0], "Normal")
            self.assertTrue(bool(mat.get("explanation")), f"Missing explanation for {topics[0]}")
            self.assertTrue(len(mat.get("quiz", [])) >= 2, f"Missing quiz for {topics[0]}")

    def test_teaching_first_and_quiz_revision_flow(self):
        graph = build_ai_tutor_graph()
        config = {"configurable": {"thread_id": "test_flow_thread_1"}}
        
        # 1. Start with custom topics
        initial_input = {
            "student": {
                "name": "Himaja",
                "subject": "Operating Systems",
                "level": "Beginner",
                "goal": "Exam",
                "available_time": "2 hours/day",
                "topics": ["Processes & Threads", "Deadlocks & Prevention"]
            },
            "completed_topics": [],
            "parallel_checks": [],
            "quiz_history": [],
            "max_quiz_attempts": 2,
            "error_count": 0,
            "needs_revision": False,
            "current_difficulty": "Normal"
        }
        
        # Stream until plan approval
        for _ in graph.stream(initial_input, config):
            pass
            
        snap = graph.get_state(config)
        self.assertEqual(snap.tasks[0].interrupts[0].value["action"], "review_learning_plan")
        
        # 2. Approve plan -> should run teaching_node and pause at take_quiz
        for _ in graph.stream(Command(resume={"approved": True}), config):
            pass
            
        snap = graph.get_state(config)
        self.assertEqual(snap.tasks[0].interrupts[0].value["action"], "take_quiz")
        
        # CRITICAL CHECK: Teaching content is generated and present before quiz is answered!
        teaching_content = snap.values.get("teaching_content")
        self.assertIsNotNone(teaching_content)
        self.assertEqual(snap.values.get("current_topic"), "Processes & Threads")
        self.assertTrue(bool(teaching_content.get("explanation")))
        self.assertTrue(len(teaching_content.get("concepts", [])) > 0)
        
        # 3. Simulate failing the quiz (wrong answers) -> score = 0%
        for _ in graph.stream(Command(resume={"answers": [3, 3]}), config):
            pass
            
        snap_after_fail = graph.get_state(config)
        # Should be in revision for the SAME topic!
        self.assertTrue(snap_after_fail.values.get("needs_revision"))
        self.assertEqual(snap_after_fail.values.get("current_topic"), "Processes & Threads")
        self.assertEqual(snap_after_fail.values.get("quiz_attempts_for_topic"), 1)
        self.assertTrue(snap_after_fail.values.get("teaching_content", {}).get("is_revision"))
        
        # 4. Simulate passing the revision quiz (correct answers) -> score = 100%
        for _ in graph.stream(Command(resume={"answers": [0, 0]}), config):
            pass
            
        snap_after_pass = graph.get_state(config)
        # Should have completed "Processes & Threads" and moved to next topic "Deadlocks & Prevention"!
        self.assertIn("Processes & Threads", snap_after_pass.values.get("completed_topics"))
        self.assertEqual(snap_after_pass.values.get("current_topic"), "Deadlocks & Prevention")
        self.assertFalse(snap_after_pass.values.get("needs_revision"))
        # Teaching content for Deadlocks & Prevention must be populated!
        self.assertTrue(bool(snap_after_pass.values.get("teaching_content", {}).get("explanation")))


if __name__ == "__main__":
    unittest.main()
