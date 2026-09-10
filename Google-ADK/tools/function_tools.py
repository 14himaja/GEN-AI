# Import ADK Agent
from google.adk.agents import Agent


# Create a custom function tool
def calculate_area(radius: float) -> dict:
    """Calculate the area of a circle using its radius."""

    # Calculate circle area
    area = 3.14 * radius * radius

    # Return the result
    return {
        "status": "success",
        "area": area
    }


# Create the ADK agent
root_agent = Agent(
    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent name
    name="math_agent",

    # Agent instructions
    instruction="Use the calculate_area tool when the user asks for a circle's area.",

    # Give the function to the agent as a tool
    tools=[calculate_area],
)