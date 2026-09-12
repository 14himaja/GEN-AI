"""
Main LangGraph Construction for AI Personal Tutor.
==================================================
Demonstrates:
1. StateGraph: Core graph container parameterized by TutorState.
2. START & END: Entry and exit points.
3. Sequential Edges: Step-by-step pipeline from start to assessment, planning, approval.
4. Parallel Execution (Fan-out / Fan-in):
   Teaching -> [Concept Check, Example Check, Exam Check] -> Parallel Merge.
5. Conditional Edges (Dynamic Routing):
   - Approval check: Approve -> Topic Selection / Reject -> Re-plan.
   - Topic availability check: Topics remaining -> Teaching / Finished -> Final Assessment.
   - Quiz score check: Pass -> Next Topic / Fail -> Revision Loop.
6. Iterative Cycles: Revision -> Quiz retry loop.
7. Persistence & Checkpointing: MemorySaver preserving graph state across executions.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from ai_tutor.core.state import TutorState
from ai_tutor.core.nodes import (
    initial_assessment_node,
    learning_planner_node,
    human_approval_node,
    topic_selection_node,
    teaching_node,
    concept_check_node,
    example_check_node,
    exam_check_node,
    parallel_merge_node,
    quiz_node,
    evaluation_node,
    revision_node,
    final_assessment_node
)


# ---------------------------------------------------------------------------
# 1. Conditional Edge Router Functions
# ---------------------------------------------------------------------------

def route_human_approval(state: TutorState) -> Literal["topic_selection", "learning_planner"]:
    """
    Conditional Edge #1:
    Checks if human approved the proposed learning plan.
    - If Approved -> proceed to Topic Selection.
    - If Not Approved -> return to Learning Planner to regenerate.
    """
    if state.get("plan_approved", True):
        return "topic_selection"
    return "learning_planner"


def route_topic_selection(state: TutorState) -> Literal["teaching", "final_assessment"]:
    """
    Conditional Edge #2:
    Dynamic routing based on remaining curriculum topics.
    - If a topic is available to study -> route to Teaching Node.
    - If all topics are completed -> route to Final Assessment.
    """
    current_topic = state.get("current_topic")
    if current_topic:
        return "teaching"
    return "final_assessment"


def route_after_quiz(state: TutorState) -> Literal["topic_selection", "revision"]:
    """
    Conditional Edge #3:
    Decides between moving forward or entering the adaptive revision loop.
    - Score >= 70% or max attempts -> route to Topic Selection (Next Topic).
    - Score < 70% -> route to Revision Node (Cycle back!).
    """
    if state.get("needs_revision", False):
        return "revision"
    return "topic_selection"


# ---------------------------------------------------------------------------
# 2. Graph Construction Function
# ---------------------------------------------------------------------------

def build_ai_tutor_graph(checkpointer: MemorySaver = None):
    """
    Builds and compiles the complete LangGraph StateGraph.
    
    Graph Architecture Diagram:
    
                        START
                          │
                  initial_assessment
                          │
                   learning_planner <──┐ (if modified)
                          │            │
                    human_approval ────┘
                          │ (if approved)
                   topic_selection <─────────────────┐
                     │          │                    │
        (has topic)  │          │ (all done)         │
                     ▼          ▼                    │
                  teaching   final_assessment        │
                     │          │                    │
         ┌───────────┼───────────┐                   │
         ▼           ▼           ▼                   │
      concept     example       exam                 │
       check       check       check                 │
         └───────────┼───────────┘                   │
                     ▼                               │
               parallel_merge                        │
                     │                               │
                   quiz <──────────────┐             │
                     │                 │             │
                evaluation             │ (retry)     │
                     │                 │             │
          ┌──────────┴──────────┐      │             │
   (fail) │                     │ (pass)             │
          ▼                     └────────────────────┘
       revision ───────────────────────┘
    """
    builder = StateGraph(TutorState)
    
    # -----------------------------------------------------------------------
    # Step A: Register all Nodes
    # -----------------------------------------------------------------------
    builder.add_node("initial_assessment", initial_assessment_node)
    builder.add_node("learning_planner", learning_planner_node)
    builder.add_node("human_approval", human_approval_node)
    builder.add_node("topic_selection", topic_selection_node)
    builder.add_node("teaching", teaching_node)
    
    # Parallel evaluation nodes (Reducer merges their outputs)
    builder.add_node("concept_check", concept_check_node)
    builder.add_node("example_check", example_check_node)
    builder.add_node("exam_check", exam_check_node)
    builder.add_node("parallel_merge", parallel_merge_node)
    
    # Quiz, Evaluation & Revision nodes
    builder.add_node("quiz", quiz_node)
    builder.add_node("evaluation", evaluation_node)
    builder.add_node("revision", revision_node)
    
    # Final assessment node
    builder.add_node("final_assessment", final_assessment_node)
    
    # -----------------------------------------------------------------------
    # Step B: Connect Edges
    # -----------------------------------------------------------------------
    
    # 1. Entry Point & Sequential flow
    builder.add_edge(START, "initial_assessment")
    builder.add_edge("initial_assessment", "learning_planner")
    builder.add_edge("learning_planner", "human_approval")
    
    # 2. Conditional edge after Human Approval
    builder.add_conditional_edges(
        "human_approval",
        route_human_approval,
        {
            "topic_selection": "topic_selection",
            "learning_planner": "learning_planner"
        }
    )
    
    # 3. Conditional edge after Topic Selection: Teach vs Final
    builder.add_conditional_edges(
        "topic_selection",
        route_topic_selection,
        {
            "teaching": "teaching",
            "final_assessment": "final_assessment"
        }
    )
    
    # 4. PARALLEL EXECUTION (Fan-Out from teaching to 3 check nodes)
    builder.add_edge("teaching", "concept_check")
    builder.add_edge("teaching", "example_check")
    builder.add_edge("teaching", "exam_check")
    
    # 5. PARALLEL MERGE (Fan-In from 3 check nodes to merge node)
    builder.add_edge("concept_check", "parallel_merge")
    builder.add_edge("example_check", "parallel_merge")
    builder.add_edge("exam_check", "parallel_merge")
    
    # 6. Sequential flow from Parallel Merge into Quiz & Evaluation
    builder.add_edge("parallel_merge", "quiz")
    builder.add_edge("quiz", "evaluation")
    
    # 7. CONDITIONAL ROUTING & ITERATIVE REVISION LOOP
    builder.add_conditional_edges(
        "evaluation",
        route_after_quiz,
        {
            "topic_selection": "topic_selection",
            "revision": "revision"
        }
    )
    
    # 8. Revision cycles back directly into the Quiz node!
    builder.add_edge("revision", "quiz")
    
    # 9. Final Assessment leads to graph termination
    builder.add_edge("final_assessment", END)
    
    # -----------------------------------------------------------------------
    # Step C: Compile with Checkpointer (Persistence & Memory)
    # -----------------------------------------------------------------------
    if checkpointer is None:
        checkpointer = MemorySaver()
        
    compiled_app = builder.compile(checkpointer=checkpointer)
    return compiled_app


# Global compiled app with default in-memory checkpointer
tutor_graph = build_ai_tutor_graph()
