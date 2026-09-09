# Import Agent from Google ADK
from google.adk.agents.llm_agent import Agent

# Create the root/main agent
root_agent = Agent(
    # Model used by the agent
    model="gemini-2.5-flash",

    # Name of the agent
    name="root_agent",

    # What the agent does
    description="A helpful assistant for user questions.",

    # Instructions for the agent
    instruction="Answer user questions to the best of your knowledge.",
)