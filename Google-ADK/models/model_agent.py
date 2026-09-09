# Import ADK Agent
from google.adk.agents import Agent

# Import LiteLlm model wrapper
from google.adk.models.lite_llm import LiteLlm

# Load environment variables
import dotenv
dotenv.load_dotenv()

# Import os to read API key
import os

# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI model through LiteLlm
model_openAI = LiteLlm(
    model="openai/gpt-4o",
    api_key=api_key,
    temperature=0.7,
    max_tokens=10,
)

# Create ADK agent
root_agent = Agent(
    # Use the OpenAI model
    model=model_openAI,

    # Agent name
    name="root_agent",

    # Agent purpose
    description="A helpful assistant for user questions.",

    # Agent instructions
    instruction="Answer user questions to the best of your knowledge",
)