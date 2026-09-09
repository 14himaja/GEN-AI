# Import ADK Agent
from google.adk.agents import Agent

# Import LiteLlm wrapper
from google.adk.models.lite_llm import LiteLlm

# Load environment variables
import dotenv
dotenv.load_dotenv()

# Import os to read API key
import os

# Create OpenRouter model
openrouter_model = LiteLlm(
    model="openrouter/deepseek/deepseek-chat-v3.1:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Create ADK agent
root_agent = Agent(
    # Use OpenRouter model
    model=openrouter_model,

    # Agent name
    name="root_agent",

    # Agent purpose
    description="A helpful assistant for user questions.",

    # Agent instructions
    instruction="Answer user questions to the best of your knowledge",
)