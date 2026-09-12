# AI Personal Tutor — LangGraph Adaptive Learning System

An intelligent, stateful **AI Personal Tutor** built with **LangGraph**, **FastAPI**, and a **modern web UI**. Rather than being a generic question-answering bot, the tutor behaves like an adaptive teacher whose workflow changes dynamically based on student assessment, human feedback, quiz scores, and learning progress.

---

## Quick Start (Single Command)

### 1. Launch the Application
Run the launcher from the project root:

```bash
python ai_tutor/run.py
```

### 2. Open the Interactive Web App
Visit in your browser:
* **Web UI Dashboard**: [http://localhost:8000](http://localhost:8000)
* **Interactive API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Automated Tests
```bash
python ai_tutor/tests/test_graph.py
```

---

## LangGraph Concepts Masterclass (Beginner-Friendly)

Every core LangGraph concept is intentionally implemented in this project with clean, simple code:

### 1. StateGraph, START, and END (`ai_tutor/core/graph.py`)
* `StateGraph`: The primary container that holds nodes and defines how state transitions between them.
* `START`: The official entry point where input parameters first enter the graph.
* `END`: The terminal point signifying that the curriculum is finished.

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(TutorState)
builder.add_edge(START, "initial_assessment")
builder.add_edge("final_assessment", END)
```

---

### 2. TypedDict State & Pydantic Validation (`ai_tutor/core/state.py`)
* **`TutorState` (TypedDict)**: The shared dictionary that travels between nodes. Every node reads from it and returns updates to it.
* **Pydantic Models**: Ensure structured data validation for student profiles, quiz questions, and final reports.

```python
class StudentProfile(BaseModel):
    name: str = "Himaja"
    subject: str = "DBMS"
    level: str = "Beginner"

class TutorState(TypedDict, total=False):
    student: Dict[str, Any]
    learning_plan: List[str]
    parallel_checks: Annotated[List[str], operator.add]  # Reducer!
    completed_topics: List[str]
```

---

### 3. Reducers (`Annotated[..., operator.add]`)
When multiple nodes execute in parallel, writing to the same state key would normally overwrite previous values. A **Reducer** defines how updates should combine.
Using `operator.add`, LangGraph automatically concatenates outputs from parallel branches into a single aggregated list:

```python
import operator
from typing import Annotated, List

# Each parallel worker appends its evaluation without clobbering others:
parallel_checks: Annotated[List[str], operator.add]
```

---

### 4. Parallel Execution (Fan-Out / Fan-In)
After the `teaching` node generates a lesson, three independent evaluation nodes execute concurrently:
1. `concept_check`: Evaluates theoretical definition.
2. `example_check`: Verifies practical application.
3. `exam_check`: Identifies tricky exam patterns.

```python
# Fan-out: One node connects to multiple parallel nodes
builder.add_edge("teaching", "concept_check")
builder.add_edge("teaching", "example_check")
builder.add_edge("teaching", "exam_check")

# Fan-in: Parallel nodes converge at parallel_merge
builder.add_edge("concept_check", "parallel_merge")
builder.add_edge("example_check", "parallel_merge")
builder.add_edge("exam_check", "parallel_merge")
```

---

### 5. Subgraphs (`ai_tutor/core/quiz_subgraph.py`)
A **Subgraph** is an independent `StateGraph` encapsulated as a modular unit. The main tutor graph calls the `quiz_subgraph` whenever a topic requires question generation and grading:

```python
subgraph_builder = StateGraph(QuizSubState)
subgraph_builder.add_node("generate_quiz", generate_quiz_node)
subgraph_builder.add_node("grade_quiz", grade_quiz_node)
quiz_subgraph = subgraph_builder.compile()
```

---

### 6. Human-in-the-Loop & Interrupts (`interrupt()` & `Command`)
LangGraph allows pausing the state machine at any node to wait for human intervention:
1. **Plan Approval**: The graph pauses so the student can review or customize their learning plan.
2. **Quiz Taking**: The graph pauses to collect the student's answers.

```python
from langgraph.types import interrupt, Command

# Inside node: Pause execution and await human input
user_feedback = interrupt({
    "action": "review_learning_plan",
    "plan": state["learning_plan"]
})

# Resuming from outside (e.g., via FastAPI):
app.stream(Command(resume={"approved": True}), config)
```

---

### 7. Conditional Edges & Dynamic Routing
Edges can decide which node to visit next based on state properties:
* **Plan Route**: If approved ➔ proceed to `topic_selection`; if modified ➔ cycle to `learning_planner`.
* **Topic Route**: If topics remain ➔ route to `teaching`; if all finished ➔ route to `final_assessment`.
* **Quiz Route**: If score &ge; 70% ➔ `topic_selection`; if score &lt; 70% ➔ `revision`.

```python
def route_after_quiz(state: TutorState):
    if state.get("needs_revision", False):
        return "revision"
    return "topic_selection"

builder.add_conditional_edges("evaluation", route_after_quiz, {
    "topic_selection": "topic_selection",
    "revision": "revision"
})
```

---

### 8. Adaptive Revision Loop (Graph Cycles)
Unlike a static linear chain, LangGraph easily expresses **cycles**:
```text
Evaluation ➔ Score < 70% ➔ Revision ➔ New Quiz ➔ Evaluation ➔ Passed?
```
The graph continues cycling until the student passes or reaches the configured `max_quiz_attempts`.

---

### 9. Checkpointing & Persistence (`MemorySaver`)
Every transition is saved using a persistent checkpointer identified by a `thread_id`:
```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# Sessions can pause, reload, or inspect history anytime:
config = {"configurable": {"thread_id": "session-101"}}
history = app.get_state_history(config)
```

---

## Complete Graph Architecture

```text
                     START
                       │
               initial_assessment
                       │
                learning_planner <──┐ (if modified)
                       │            │
          [HITL] human_approval ────┘
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
     [SUBGRAPH]  quiz <──────────────┐            │
                  │                  │            │
             evaluation              │ (retry)    │
                  │                  │            │
       ┌──────────┴──────────┐       │            │
(fail) │                     │ (pass)             │
       ▼                     └────────────────────┘
    revision ───────────────────────┘
```

---

## File Structure

```text
ai_tutor/
├── core/
│   ├── __init__.py
│   ├── state.py            # TypedDict TutorState, Pydantic models, Reducer
│   ├── knowledge.py        # Diagnostic questions, DBMS curriculum & generator
│   ├── quiz_subgraph.py    # Subgraph for Quiz generation and grading
│   ├── nodes.py            # All graph nodes with clear beginner comments
│   └── graph.py            # StateGraph builder, conditional routing, checkpointing
├── api/
│   ├── __init__.py
│   └── main.py             # FastAPI backend with session & resume endpoints
├── static/
│   ├── index.html          # Modern visual dashboard & pipeline tracker
│   ├── style.css           # Glassmorphic dark styling & responsive UI
│   └── app.js              # Frontend controller communicating with FastAPI
├── tests/
│   └── test_graph.py       # Unit tests verifying all LangGraph concepts
├── run.py                  # One-command server runner
└── README.md               # Concept guide & documentation
```
