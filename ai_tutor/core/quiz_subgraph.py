"""
Quiz Subgraph Module for LangGraph AI Tutor.
============================================
Demonstrates:
1. Subgraphs: Encapsulating a standalone multi-step workflow inside a separate StateGraph.
2. Modularity: Main graph delegates quiz generation, answer checking, and grading
   to this specialized subgraph.
3. Subgraph State: Own TypedDict state schema separate from the parent graph.
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from ai_tutor.core.knowledge import get_teaching_material


# ---------------------------------------------------------------------------
# 1. Subgraph State Definition
# ---------------------------------------------------------------------------

class QuizSubState(TypedDict, total=False):
    """
    Dedicated state for the Quiz Subgraph.
    Isolated from parent graph state; only receives what it needs.
    """
    topic: str
    difficulty: str
    is_revision: bool
    questions: List[Dict[str, Any]]
    answers: List[int]
    score: int
    correct_count: int
    total_questions: int
    feedback: str
    passed: bool
    weak_concepts: List[str]
    strong_concepts: List[str]
    review_details: List[Dict[str, Any]]


# ---------------------------------------------------------------------------
# 2. Subgraph Nodes
# ---------------------------------------------------------------------------

def distribute_question_options(q_dict: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
    """
    Evenly distributes options so the correct answer is not predictably always option 0.
    """
    opts = list(q_dict.get("options", []))
    orig_idx = q_dict.get("correct_option", 0)
    if not opts or orig_idx >= len(opts) or len(opts) < 2:
        return q_dict
        
    correct_text = opts[orig_idx]
    # Rotate target position deterministically based on question id and index
    target_pos = (q_dict.get("id", index + 1) + index) % len(opts)
    if target_pos == orig_idx:
        return q_dict
        
    opts.pop(orig_idx)
    opts.insert(target_pos, correct_text)
    
    updated_q = dict(q_dict)
    updated_q["options"] = opts
    updated_q["correct_option"] = target_pos
    return updated_q


def generate_quiz_node(state: QuizSubState) -> Dict[str, Any]:
    """
    Step 1 in Subgraph:
    Pulls questions appropriate for the current topic, difficulty, and revision state,
    and distributes options so correct answers are balanced across choices.
    """
    topic = state.get("topic", "General Topic")
    difficulty = state.get("difficulty", "Normal")
    is_revision = state.get("is_revision", False)
    
    material = get_teaching_material(topic, difficulty)
    
    # If this is a revision attempt, use specialized revision questions!
    if is_revision and "revision_quiz" in material:
        raw_questions = material["revision_quiz"]
    else:
        raw_questions = material["quiz"]
        
    distributed = [distribute_question_options(q, idx) for idx, q in enumerate(raw_questions)]
        
    return {
        "questions": distributed,
        "total_questions": len(distributed)
    }


def grade_quiz_node(state: QuizSubState) -> Dict[str, Any]:
    """
    Step 2 in Subgraph:
    Compares student answers against correct options, calculates percentage,
    identifies strong vs. weak concepts, and compiles question-by-question review
    details containing student answers, correct solutions, and explanations.
    """
    questions = state.get("questions", [])
    answers = state.get("answers", [])
    topic = state.get("topic", "General Topic")
    
    if not questions:
        return {
            "score": 0,
            "correct_count": 0,
            "total_questions": 0,
            "passed": False,
            "feedback": "No questions were found to grade.",
            "weak_concepts": ["Missing Topic Material"],
            "strong_concepts": [],
            "review_details": []
        }
    
    correct_count = 0
    weak = []
    strong = []
    review_details = []
    
    for i, q in enumerate(questions):
        student_ans = answers[i] if i < len(answers) else -1
        correct_ans = q.get("correct_option", 0)
        options = q.get("options", [])
        
        student_ans_text = options[student_ans] if (0 <= student_ans < len(options)) else "Not Answered"
        correct_ans_text = options[correct_ans] if (0 <= correct_ans < len(options)) else "N/A"
        is_correct = (student_ans == correct_ans)
        
        q_text = q.get("question", f"Question {i + 1}")
        q_label = f"Q{q.get('id', i+1)}: {q_text[:35]}..."
        
        if is_correct:
            correct_count += 1
            strong.append(q_label)
        else:
            weak.append(q_label)
            
        explanation = q.get("explanation", "")
        if not explanation:
            explanation = f"'{correct_ans_text}' is the verified solution for this concept in {topic}."
            
        review_details.append({
            "question_id": q.get("id", i + 1),
            "question": q_text,
            "options": options,
            "student_answer": student_ans,
            "student_answer_text": student_ans_text,
            "correct_answer": correct_ans,
            "correct_answer_text": correct_ans_text,
            "is_correct": is_correct,
            "explanation": explanation
        })
            
    total = len(questions)
    score_pct = int((correct_count / total) * 100) if total > 0 else 0
    passed = score_pct >= 70
    
    if passed:
        feedback = f"Excellent! You scored {score_pct}% ({correct_count}/{total} correct). Ready to advance!"
    else:
        feedback = f"Score: {score_pct}% ({correct_count}/{total} correct). Passing threshold is 70%."
        
    return {
        "score": score_pct,
        "correct_count": correct_count,
        "total_questions": total,
        "passed": passed,
        "feedback": feedback,
        "weak_concepts": weak,
        "strong_concepts": strong,
        "review_details": review_details
    }


# ---------------------------------------------------------------------------
# 3. Build and Compile Subgraph
# ---------------------------------------------------------------------------

def create_quiz_subgraph():
    """
    Creates and compiles the Quiz Subgraph.
    
    Flow:
    START -> generate_quiz_node -> grade_quiz_node -> END
    """
    subgraph_builder = StateGraph(QuizSubState)
    
    # Add nodes
    subgraph_builder.add_node("generate_quiz", generate_quiz_node)
    subgraph_builder.add_node("grade_quiz", grade_quiz_node)
    
    # Add edges
    subgraph_builder.add_edge(START, "generate_quiz")
    subgraph_builder.add_edge("generate_quiz", "grade_quiz")
    subgraph_builder.add_edge("grade_quiz", END)
    
    return subgraph_builder.compile()


# Pre-compiled instance ready for use in the main graph
quiz_subgraph = create_quiz_subgraph()
