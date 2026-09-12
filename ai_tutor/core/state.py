"""
State Definitions for AI Personal Tutor.
=========================================
Demonstrates:
1. Pydantic Models: Structured data validation for student profile, questions, and quiz results.
2. TypedDict State: The main LangGraph state dictionary passed between nodes.
3. Reducers: Using `Annotated[list[str], operator.add]` to automatically aggregate
   results from parallel nodes without overwriting.
"""

from typing import TypedDict, Optional, List, Dict, Any, Annotated
import operator
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# 1. Pydantic Models (Structured Data)
# ---------------------------------------------------------------------------

class StudentProfile(BaseModel):
    """Stores initial student inputs."""
    name: str = Field(default="Himaja", description="Name of the student")
    subject: str = Field(default="DBMS", description="Subject to study")
    goal: str = Field(default="Prepare for semester exam", description="Learning goal")
    level: str = Field(default="Beginner", description="Current knowledge level: Beginner, Intermediate, Advanced")
    available_time: Optional[str] = Field(default="Self-paced", description="Study time available")
    topics: List[str] = Field(default_factory=list, description="Optional custom topics list")


class QuizQuestion(BaseModel):
    """Structure for an individual quiz question."""
    id: int
    question: str
    options: List[str]
    correct_option: int  # 0-indexed option index
    explanation: str


class QuizResult(BaseModel):
    """Result returned by the Quiz Subgraph."""
    topic: str
    score: int  # 0 to 100 percentage
    total_questions: int
    correct_count: int
    feedback: str
    passed: bool
    weak_concepts: List[str] = Field(default_factory=list)
    strong_concepts: List[str] = Field(default_factory=list)


class FinalReport(BaseModel):
    """Overall report generated when student completes the curriculum."""
    student_name: str
    subject: str
    overall_score: int
    topics_completed: List[str]
    strong_areas: List[str]
    weak_areas: List[str]
    total_quiz_attempts: int
    improvement_percentage: int
    recommended_revision: List[str]
    summary_message: str


def topic_checks_reducer(existing: List[str], new: List[str]) -> List[str]:
    """
    Custom LangGraph Reducer:
    Aggregates parallel worker outputs for the current topic.
    Keeps only the latest 3 checks (Concept, Example, Exam) to avoid accumulating across topics.
    """
    if not new:
        return []
    combined = (existing or []) + new
    return combined[-3:]


# ---------------------------------------------------------------------------
# 2. Main LangGraph State (TypedDict)
# ---------------------------------------------------------------------------

class TutorState(TypedDict, total=False):
    """
    Main state for the AI Personal Tutor StateGraph.
    
    Every node in the graph receives this state and returns updates to it.
    LangGraph merges the returned dictionary back into the state.
    """
    # Student profile and inputs
    student: Dict[str, Any]
    
    # Assessment & Knowledge tracking
    initial_assessment_done: bool
    initial_score: int
    strong_topics: List[str]
    weak_topics: List[str]
    current_knowledge_level: str  # Beginner, Intermediate, Advanced
    
    # Curriculum & Learning plan
    learning_plan: List[str]
    plan_approved: bool           # Controlled via Human-in-the-Loop
    human_feedback: Optional[str] # Reviewer comments if modified
    
    # Topic iteration tracking
    completed_topics: List[str]
    current_topic: Optional[str]
    current_topic_index: int
    
    # Current teaching materials
    teaching_content: Dict[str, Any]
    
    # PARALLEL EXECUTION REDUCER:
    # Aggregates parallel outputs for the current topic without leaking across topics!
    parallel_checks: Annotated[List[str], topic_checks_reducer]
    
    # Quiz & Evaluation State (from Subgraph)
    current_quiz: List[Dict[str, Any]]
    student_answers: List[int]
    quiz_attempts_for_topic: int
    last_quiz_result: Optional[Dict[str, Any]]
    quiz_history: List[Dict[str, Any]]
    
    # Adaptive difficulty tracking
    current_difficulty: str       # Easy, Normal, Advanced
    
    # Workflow control & Revision loop flags
    needs_revision: bool
    max_quiz_attempts: int
    
    # Error handling & Recovery
    error_count: int
    last_error_message: Optional[str]
    
    # Final assessment & report
    final_report: Optional[Dict[str, Any]]
    
    # Step-by-step audit log for UI visualization
    node_history: Annotated[List[str], operator.add]
