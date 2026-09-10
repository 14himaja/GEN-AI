# Import ADK Agent
from google.adk.agents import Agent


# Create research agent
research_agent = Agent(
    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent name
    name="research_agent",

    # Agent purpose
    description="Researches information for the user.",

    # Agent instructions
    instruction="Research the topic and provide useful information.",
)


# Create writing agent
writing_agent = Agent(
    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent name
    name="writing_agent",

    # Agent purpose
    description="Writes content using research information.",

    # Agent instructions
    instruction="Create clear content based on the available information.",
)


# Create the main agent
root_agent = Agent(
    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent name
    name="manager_agent",

    # Agent purpose
    description="Coordinates research and writing tasks.",

    # Main instructions
    instruction="Coordinate the research and writing agents to complete the user's request.",

    # Add specialist agents
    sub_agents=[
        research_agent,
        writing_agent,
    ],
)