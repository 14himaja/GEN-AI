# Import ADK Agent
from google.adk.agents import Agent

# Import LiteLlm wrapper
from google.adk.models.lite_llm import LiteLlm

# Create Ollama model
ollama_model = LiteLlm(
    model="ollama_chat/llama3.2"
)

# Create ADK agent
root_agent = Agent(
    # Use Ollama model
    model=ollama_model,

    # Agent name
    name="root_agent",

    # Agent purpose
    description="A helpful assistant for user questions.",

    # Agent instructions
    instruction="Answer user questions to the best of your knowledge",
)