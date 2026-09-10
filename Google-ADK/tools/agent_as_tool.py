# Import ADK Agent
from google.adk.agents import Agent

# Import AgentTool
from google.adk.tools import AgentTool


# Create a specialist agent
resume_agent = Agent(
    # Model used
    model="gemini-2.0-flash",

    # Agent name
    name="resume_agent",

    # Specialist instructions
    instruction="Help users improve their resumes.",
)


# Convert the agent into a tool
resume_tool = AgentTool(agent=resume_agent)


# Create the main agent
root_agent = Agent(
    # Model used
    model="gemini-2.0-flash",

    # Agent name
    name="career_agent",

    # Main instructions
    instruction="Help users with career questions. Use the resume agent for resume-related questions.",

    # Give the specialist agent as a tool
    tools=[resume_tool],
)