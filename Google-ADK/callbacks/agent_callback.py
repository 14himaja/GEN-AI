from datetime import datetime

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext


def before_agent_callback(callback_context: CallbackContext):

    # Access session state
    state = callback_context.state

    # Count requests
    if "request_count" not in state:
        state["request_count"] = 1
    else:
        state["request_count"] += 1

    # Store start time
    state["start_time"] = datetime.now()

    print("Agent started")
    print("Request:", state["request_count"])

    return None


def after_agent_callback(callback_context: CallbackContext):

    # Access session state
    state = callback_context.state

    # Calculate execution time
    end_time = datetime.now()

    duration = (
        end_time - state["start_time"]
    ).total_seconds()

    print("Agent finished")
    print("Duration:", duration, "seconds")

    return None


root_agent = Agent(
    model="gemini-2.0-flash",
    name="callback_agent",

    instruction="Answer the user's question.",

    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)