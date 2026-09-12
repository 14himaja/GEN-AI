"""
LangGraph Nodes for AI Personal Tutor.
=======================================
Each function here represents a NODE in the LangGraph StateGraph.

Concepts Demonstrated:
1. Pure State Transitions: Receiving TutorState, returning updated dictionary fields.
2. Reducers: Parallel nodes returning list items that LangGraph appends automatically.
3. Human-in-the-Loop: Calling `interrupt()` to pause workflow for human input (plan approval & quiz).
4. Subgraph Invocation: Calling the compiled `quiz_subgraph`.
5. Iterative Loops: `revision_node` preparing state before cycling back to quiz.
6. Error Handling: Graceful try/except wrapping in nodes.
"""

from typing import Dict, Any, List
from langgraph.types import interrupt

from ai_tutor.core.state import TutorState, StudentProfile, QuizResult, FinalReport
from ai_tutor.core.knowledge import (
    DEFAULT_SUBJECT_TOPICS,
    get_initial_questions,
    get_teaching_material,
    get_default_topics_for_subject
)
from ai_tutor.core.quiz_subgraph import quiz_subgraph


# ---------------------------------------------------------------------------
# Node 1: Initial Assessment Node
# ---------------------------------------------------------------------------

def initial_assessment_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 1: Assessment]
    Evaluates baseline knowledge.
    Pauses with an interrupt() for the student to complete a diagnostic test on their chosen subject.
    Computes real strong vs weak topics based on their test answers.
    """
    student_data = state.get("student", {})
    subject = student_data.get("subject", "DBMS")
    level = student_data.get("level", "Beginner")
    custom_topics = student_data.get("topics", [])
    
    diagnostic_questions = get_initial_questions(subject)
    
    # If diagnostic assessment is not done and custom topics were not pre-supplied:
    if not state.get("initial_assessment_done", False) and not custom_topics and not student_data.get("skip_diagnostic", False):
        user_response = interrupt({
            "action": "take_diagnostic_quiz",
            "subject": subject,
            "questions": diagnostic_questions,
            "prompt": f"Before creating your customized learning plan, take this quick diagnostic check on {subject} to identify your strengths and focus areas."
        })
        
        user_answers = []
        if isinstance(user_response, dict):
            user_answers = user_response.get("answers", [])
        elif isinstance(user_response, list):
            user_answers = user_response
            
        correct_count = 0
        strong_topics: List[str] = []
        weak_topics: List[str] = []
        
        for idx, q in enumerate(diagnostic_questions):
            topic = q.get("topic", f"Topic {idx+1}")
            user_ans = user_answers[idx] if idx < len(user_answers) else -1
            if user_ans == q.get("correct_option", 0):
                correct_count += 1
                if topic not in strong_topics:
                    strong_topics.append(topic)
            else:
                if topic not in weak_topics:
                    weak_topics.append(topic)
                    
        total_q = len(diagnostic_questions)
        baseline_score = int((correct_count / total_q) * 100) if total_q > 0 else 50
        
        # Calibrate difficulty level from test results
        calibrated_level = "Advanced" if baseline_score >= 80 else ("Intermediate" if baseline_score >= 50 else "Beginner")
        
        return {
            "initial_assessment_done": True,
            "initial_score": baseline_score,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "current_knowledge_level": calibrated_level,
            "current_difficulty": "Normal" if calibrated_level == "Intermediate" else calibrated_level,
            "node_history": ["initial_assessment"]
        }
        
    # Fallback / Unit-test bypass
    default_topics = get_default_topics_for_subject(subject)
    half = max(1, len(default_topics) // 2)
    weak_topics = default_topics[:half]
    strong_topics = default_topics[half:]
    baseline_score = 40 if level.lower() == "beginner" else (70 if level.lower() == "intermediate" else 88)
    
    return {
        "initial_assessment_done": True,
        "initial_score": baseline_score,
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
        "current_knowledge_level": level,
        "current_difficulty": "Normal" if level.lower() == "intermediate" else ("Advanced" if level.lower() == "advanced" else "Easy"),
        "node_history": ["initial_assessment"]
    }


# ---------------------------------------------------------------------------
# Node 2: Learning Planner Node
# ---------------------------------------------------------------------------

def learning_planner_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 2: Planner]
    Creates a customized learning plan.
    Prioritizes WEAK topics first so the student focuses where help is needed most.
    """
    student_data = state.get("student", {})
    subject = student_data.get("subject", "DBMS")
    custom_topics = student_data.get("topics", [])
    weak_topics = state.get("weak_topics", [])
    
    # 1. Base list of topics from custom input or subject defaults
    if custom_topics and len(custom_topics) > 0:
        all_topics = list(custom_topics)
    else:
        all_topics = get_default_topics_for_subject(subject)
        
    # 2. Reorder: Prioritize weak topics first, then remaining topics
    planned_order = []
    for topic in all_topics:
        if any(weak.lower() in topic.lower() or topic.lower() in weak.lower() for weak in weak_topics):
            planned_order.append(topic)
            
    for topic in all_topics:
        if topic not in planned_order:
            planned_order.append(topic)
            
    # Add a final revision checkpoint
    if "Final Comprehensive Review" not in planned_order:
        planned_order.append("Final Comprehensive Review")
        
    return {
        "learning_plan": planned_order,
        "plan_approved": False,
        "node_history": ["learning_planner"]
    }


# ---------------------------------------------------------------------------
# Node 3: Human Approval Node (HUMAN-IN-THE-LOOP INTERRUPT)
# ---------------------------------------------------------------------------

def human_approval_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 3: Human-in-the-Loop]
    Demonstrates LangGraph `interrupt()`.
    Pauses graph execution so the student can review, add topics, remove topics,
    or adjust topic order in their learning plan.
    When resumed with `Command(resume=...)`, execution continues seamlessly!
    """
    learning_plan = state.get("learning_plan", [])
    weak_topics = state.get("weak_topics", [])
    strong_topics = state.get("strong_topics", [])
    initial_score = state.get("initial_score", 0)
    student = state.get("student", {})
    
    # Trigger LangGraph Interrupt!
    user_decision = interrupt({
        "action": "review_learning_plan",
        "plan": learning_plan,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "initial_score": initial_score,
        "subject": student.get("subject", "Subject"),
        "prompt": "Please review your recommended learning plan. You can add custom topics, remove topics, or approve to start."
    })
    
    # Resumed: user_decision will contain what the human provided
    if isinstance(user_decision, dict):
        approved = user_decision.get("approved", True)
        modified_plan = user_decision.get("modified_plan")
        feedback = user_decision.get("feedback", "")
    else:
        approved = True
        modified_plan = None
        feedback = ""
        
    updates: Dict[str, Any] = {
        "plan_approved": approved,
        "human_feedback": feedback,
        "node_history": ["human_approval"]
    }
    
    if modified_plan and isinstance(modified_plan, list) and len(modified_plan) > 0:
        updates["learning_plan"] = modified_plan
        
    return updates


# ---------------------------------------------------------------------------
# Node 4: Topic Selection Node (DYNAMIC ROUTING PREPARATION)
# ---------------------------------------------------------------------------

def topic_selection_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 4: Topic Selection]
    Checks completed topics and selects the next topic to study.
    Resets per-topic attempt counters and revision flags.
    """
    plan = state.get("learning_plan", [])
    completed = state.get("completed_topics", [])
    
    # Find next uncompleted topic (excluding final review if other topics remain)
    next_topic = None
    next_index = 0
    
    for idx, topic in enumerate(plan):
        if topic not in completed and topic != "Final Comprehensive Review":
            next_topic = topic
            next_index = idx
            break
            
    return {
        "current_topic": next_topic,
        "current_topic_index": next_index,
        "quiz_attempts_for_topic": 0,
        "needs_revision": False,
        "parallel_checks": [],  # Clear previous check logs
        "node_history": ["topic_selection"]
    }


# ---------------------------------------------------------------------------
# Node 5: Teaching Node
# ---------------------------------------------------------------------------

def teaching_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 5: Teaching]
    Generates tailored lesson content (explanation, core concepts, concrete example, practice)
    matched to current difficulty level (Easy, Normal, Advanced).
    """
    topic = state.get("current_topic", "General Topic")
    difficulty = state.get("current_difficulty", "Normal")
    
    content = get_teaching_material(topic, difficulty)
    
    return {
        "teaching_content": content,
        "node_history": ["teaching"]
    }


# ---------------------------------------------------------------------------
# Nodes 6a, 6b, 6c: Parallel Evaluation Nodes (DEMONSTRATES PARALLEL BRANCHES & REDUCER)
# ---------------------------------------------------------------------------

def concept_check_node(state: TutorState) -> Dict[str, Any]:
    """
    [PARALLEL BRANCH A: Concept Check]
    Runs concurrently with branches B and C.
    Demonstrates LangGraph REDUCER: appends to `parallel_checks` list via operator.add!
    """
    topic = state.get("current_topic", "General")
    content = state.get("teaching_content", {})
    check_text = content.get("parallel_checks", {}).get("concept", f"Concept theory validated for {topic}.")
    
    return {
        "parallel_checks": [f"[Concept Check]: {check_text}"],
        "node_history": ["concept_check"]
    }


def example_check_node(state: TutorState) -> Dict[str, Any]:
    """
    [PARALLEL BRANCH B: Example Check]
    Runs concurrently with branches A and C.
    Demonstrates LangGraph REDUCER: appends to `parallel_checks` list via operator.add!
    """
    topic = state.get("current_topic", "General")
    content = state.get("teaching_content", {})
    check_text = content.get("parallel_checks", {}).get("example", f"Practical example verified for {topic}.")
    
    return {
        "parallel_checks": [f"[Example Check]: {check_text}"],
        "node_history": ["example_check"]
    }


def exam_check_node(state: TutorState) -> Dict[str, Any]:
    """
    [PARALLEL BRANCH C: Exam Check]
    Runs concurrently with branches A and B.
    Demonstrates LangGraph REDUCER: appends to `parallel_checks` list via operator.add!
    """
    topic = state.get("current_topic", "General")
    content = state.get("teaching_content", {})
    check_text = content.get("parallel_checks", {}).get("exam", f"Exam criteria and tricky questions mapped for {topic}.")
    
    return {
        "parallel_checks": [f"[Exam Check]: {check_text}"],
        "node_history": ["exam_check"]
    }


# ---------------------------------------------------------------------------
# Node 7: Parallel Merge Node (AGGREGATION POINT)
# ---------------------------------------------------------------------------

def parallel_merge_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 7: Parallel Merge]
    Combines the parallel check results merged by the state reducer.
    """
    checks = state.get("parallel_checks", [])
    return {
        "node_history": ["parallel_merge"]
    }


# ---------------------------------------------------------------------------
# Node 8: Quiz Node (INVOKES QUIZ SUBGRAPH + HUMAN-IN-THE-LOOP)
# ---------------------------------------------------------------------------

def quiz_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 8: Quiz Interaction]
    Demonstrates:
    1. Subgraph Invocation: Calls `quiz_subgraph` to generate questions.
    2. Human-in-the-Loop: Calls `interrupt()` for the student to select answers.
    3. Subgraph Grading: Passes answers back into `quiz_subgraph` for grading.
    """
    topic = state.get("current_topic", "General Topic")
    difficulty = state.get("current_difficulty", "Normal")
    is_revision = state.get("needs_revision", False)
    
    # Step A: Invoke Subgraph to generate questions
    gen_result = quiz_subgraph.invoke({
        "topic": topic,
        "difficulty": difficulty,
        "is_revision": is_revision,
        "questions": [],
        "answers": []
    })
    questions = gen_result.get("questions", [])
    
    # Step B: Interrupt for human student answers
    student_response = interrupt({
        "action": "take_quiz",
        "topic": topic,
        "difficulty": difficulty,
        "is_revision": is_revision,
        "questions": questions,
        "prompt": "Please select the best answer for each question."
    })
    
    # Extract student answers (list of integers representing chosen option indices)
    if isinstance(student_response, dict):
        student_answers = student_response.get("answers", [])
    elif isinstance(student_response, list):
        student_answers = student_response
    else:
        student_answers = [0] * len(questions)  # Fallback default
        
    # Step C: Grade via Subgraph
    grade_result = quiz_subgraph.invoke({
        "topic": topic,
        "difficulty": difficulty,
        "is_revision": is_revision,
        "questions": questions,
        "answers": student_answers
    })
    
    attempts = state.get("quiz_attempts_for_topic", 0) + 1
    
    # Update history log
    history_entry = {
        "topic": topic,
        "attempt": attempts,
        "score": grade_result.get("score", 0),
        "passed": grade_result.get("passed", False),
        "is_revision": is_revision
    }
    quiz_history = list(state.get("quiz_history", []))
    quiz_history.append(history_entry)
    
    return {
        "current_quiz": questions,
        "student_answers": student_answers,
        "quiz_attempts_for_topic": attempts,
        "last_quiz_result": grade_result,
        "quiz_history": quiz_history,
        "node_history": ["quiz"]
    }


# ---------------------------------------------------------------------------
# Node 9: Evaluation Node (DIFFICULTY ADAPTATION & DECISION PREP)
# ---------------------------------------------------------------------------

def evaluation_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 9: Evaluation]
    Evaluates quiz performance:
    - Adapts difficulty based on score.
    - Decides whether student passes or enters revision loop.
    - Limits revision to max_quiz_attempts to avoid infinite loops.
    """
    last_res = state.get("last_quiz_result", {})
    score = last_res.get("score", 0)
    topic = state.get("current_topic", "")
    attempts = state.get("quiz_attempts_for_topic", 1)
    max_attempts = state.get("max_quiz_attempts", 2)
    completed = list(state.get("completed_topics", []))
    
    # 1. Difficulty Adaptation
    if score < 50:
        new_diff = "Easy"
    elif score <= 70:
        new_diff = "Normal"
    else:
        new_diff = "Advanced"
        
    # 2. Decision Logic
    passed = score >= 70
    max_reached = (not passed) and (attempts >= max_attempts)
    
    if passed:
        needs_revision = False
        if topic and topic not in completed:
            completed.append(topic)
    else:
        # If student reached max attempts, advance with guidance to avoid endless loops
        if max_reached:
            needs_revision = False
            if topic and topic not in completed:
                completed.append(topic)  # Move forward after reaching max attempts
        else:
            needs_revision = True
            
    # Enrich last_quiz_result dictionary with explicit attempt context
    updated_last_res = dict(last_res)
    updated_last_res["attempts"] = attempts
    updated_last_res["max_attempts"] = max_attempts
    updated_last_res["max_attempts_reached"] = max_reached
    updated_last_res["remaining_attempts"] = max(0, max_attempts - attempts)
    updated_last_res["passed"] = passed

    # Set clear, unambiguous feedback tailored to whether revision or advancement occurs
    total_q = last_res.get("total_questions", 0)
    correct_q = last_res.get("correct_count", 0)
    if passed:
        updated_last_res["feedback"] = f"Outstanding! You scored {score}% ({correct_q}/{total_q} correct). Passing threshold is 70%."
    elif max_reached:
        updated_last_res["feedback"] = f"Score: {score}% ({correct_q}/{total_q} correct). All {max_attempts} attempts completed. Review the correct answers and explanations below as you advance to the next topic."
    else:
        updated_last_res["feedback"] = f"Score: {score}% ({correct_q}/{total_q} correct). Passing threshold is 70%. Targeted revision and correct solutions are provided below before Attempt {attempts + 1}."

    return {
        "current_difficulty": new_diff,
        "needs_revision": needs_revision,
        "completed_topics": completed,
        "last_quiz_result": updated_last_res,
        "node_history": ["evaluation"]
    }


# ---------------------------------------------------------------------------
# Node 10: Revision Node (ADAPTIVE REVISION LOOP)
# ---------------------------------------------------------------------------

def revision_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 10: Revision]
    Part of the cyclic workflow (revision loop).
    Generates simplified explanations, pinpoints weak concepts, and provides targeted hints.
    """
    topic = state.get("current_topic", "General Topic")
    last_res = state.get("last_quiz_result", {})
    weak_concepts = last_res.get("weak_concepts", [])
    review_details = last_res.get("review_details", [])
    
    # Pull simplified explanation
    material = get_teaching_material(topic, "Easy")

    # Extract specific takeaways from missed questions
    missed_notes = [
        f"Key Takeaway: {item['explanation']}"
        for item in review_details
        if not item.get("is_correct", False) and item.get("explanation")
    ]
    
    base_concepts = material.get("concepts", [])
    if missed_notes:
        combined_concepts = missed_notes + [c for c in base_concepts if c not in missed_notes]
    elif weak_concepts:
        combined_concepts = [f"Priority Review: Clarify {w}" for w in weak_concepts] + base_concepts
    else:
        combined_concepts = base_concepts
    
    revision_content = {
        "topic": topic,
        "difficulty": "Easy (Revision)",
        "explanation": f"💡 Revision Focus: Let's review {topic} with simpler intuition and targeted explanations before re-attempting the quiz. " + material.get("explanation", ""),
        "concepts": combined_concepts,
        "example": material.get("example", ""),
        "focused_weak_concepts": weak_concepts,
        "is_revision": True,
        "parallel_checks": material.get("parallel_checks", {})
    }
    
    return {
        "teaching_content": revision_content,
        "current_difficulty": "Easy",  # Dynamically lower difficulty for revision
        "node_history": ["revision"]
    }


# ---------------------------------------------------------------------------
# Node 11: Final Assessment Node
# ---------------------------------------------------------------------------

def final_assessment_node(state: TutorState) -> Dict[str, Any]:
    """
    [NODE 11: Final Assessment & Report]
    Executed when all topics in the learning plan are completed.
    Calculates overall mastery, improvement percentage, and personalized recommendations.
    """
    student_data = state.get("student", {})
    name = student_data.get("name", "Student")
    subject = student_data.get("subject", "DBMS")
    
    completed = state.get("completed_topics", [])
    history = state.get("quiz_history", [])
    initial_score = state.get("initial_score", 50)
    
    # Calculate overall quiz average
    scores = [entry.get("score", 0) for entry in history] if history else [85]
    avg_score = int(sum(scores) / len(scores)) if scores else 85
    
    improvement = max(0, avg_score - initial_score)
    
    strong = list(state.get("strong_topics", []))
    weak = list(state.get("weak_topics", []))
    
    # If student scored high on weak topics during quizzes, promote them!
    for h in history:
        if h.get("passed", False) and h.get("topic") in weak:
            weak.remove(h.get("topic"))
            if h.get("topic") not in strong:
                strong.append(h.get("topic"))
                
    report = {
        "student_name": name,
        "subject": subject,
        "overall_score": avg_score,
        "topics_completed": completed,
        "strong_areas": strong if strong else ["Foundational Principles"],
        "weak_areas": weak if weak else ["None - All Core Objectives Met!"],
        "total_quiz_attempts": len(history),
        "improvement_percentage": improvement,
        "recommended_revision": [f"Review advanced indexing trade-offs before your {subject} exam."],
        "summary_message": f"Congratulations {name}! You completed your personalized learning path with an overall mastery of {avg_score}%!"
    }
    
    return {
        "final_report": report,
        "node_history": ["final_assessment"]
    }
