#######################   GOOGLE SEARCH   ###############################

# Import ADK Agent
from google.adk.agents import Agent

# Import Google Search tool
from google.adk.tools import google_search


# Create the ADK agent
root_agent = Agent(
    # Use Gemini model
    model="gemini-2.0-flash",

    # Agent name
    name="search_agent",

    # Agent instructions
    instruction="Use Google Search when you need current information.",

    # Give Google Search to the agent
    tools=[google_search],
)

######                 CODE EXECUTOR

# Import ADK Agent
from google.adk.agents import Agent

# Import code execution tool
from google.adk.code_executors import BuiltInCodeExecutor


# Create the ADK agent
root_agent = Agent(
    # Use Gemini model
    model="gemini-2.0-flash",

    # Agent name
    name="code_agent",

    # Agent instructions
    instruction="Use code execution when calculations or code are required.",

    # Enable code execution
    code_executor=BuiltInCodeExecutor(),
)