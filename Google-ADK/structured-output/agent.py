# Import ADK agent
from google.adk.agents.llm_agent import LlmAgent

# Import Pydantic
from pydantic import BaseModel, Field

# Import date type
from datetime import date


# Define output structure
class TodoItem(BaseModel):
    task: str = Field(description="Task name")
    due_date: date = Field(description="YYYY-MM-DD format")
    priority: str = Field(description="low/medium/high")


# Create the Todo agent
root_agent = LlmAgent(
    # Agent name
    name="todo_agent",

    # Model used
    model="gemini-2.0-flash",

    # Instructions for the agent
    instruction="""Generate todo items in exact JSON format.
    Make sure the format is strictly followed.

    Fields:
    1. task: Task name
    2. due_date: Due date in YYYY-MM-DD format
    3. priority: Priority (low/medium/high)

    Example:
    {
        "task": "Call client",
        "due_date": "2023-10-10",
        "priority": "high"
    }
    """,

    # Define the output format
    output_schema=TodoItem,

    # Store output using this key
    output_key="todo"
)