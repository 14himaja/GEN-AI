from google.adk.agents import Agent
from google.adk.models import LlmRequest
from google.adk.models import LlmResponse


def before_model(callback_context, llm_request: LlmRequest):
    print("Model is about to run...")

    return None


def after_model(callback_context, llm_response: LlmResponse):
    print("Model finished!")

    return None


root_agent = Agent(
    model="gemini-2.0-flash",
    name="model_callback_agent",

    instruction="Answer the user's question.",

    before_model_callback=before_model,
    after_model_callback=after_model,
)