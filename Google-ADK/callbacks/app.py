from datetime import datetime

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext


# =========================================================
# TOOL
# =========================================================

def get_weather(city: str):
    """Get the weather for a city."""

    return f"The weather in {city} is sunny."


# =========================================================
# BEFORE AGENT CALLBACK
# =========================================================

def before_agent_callback(callback_context: CallbackContext):

    # Access session state
    state = callback_context.state

    # Store the time when the agent starts
    state["start_time"] = datetime.now()

    print("\n--- BEFORE AGENT ---")
    print("Agent is starting...")

    return None


# =========================================================
# AFTER AGENT CALLBACK
# =========================================================

def after_agent_callback(callback_context: CallbackContext):

    # Access session state
    state = callback_context.state

    # Get the end time
    end_time = datetime.now()

    # Calculate execution time
    duration = (
        end_time - state["start_time"]
    ).total_seconds()

    print("\n--- AFTER AGENT ---")
    print("Agent finished.")
    print("Execution time:", duration, "seconds")

    return None


# =========================================================
# BEFORE MODEL CALLBACK
# =========================================================

def before_model_callback(
    callback_context,
    llm_request
):

    print("\n--- BEFORE MODEL ---")
    print("Model is about to run.")

    return None


# =========================================================
# AFTER MODEL CALLBACK
# =========================================================

def after_model_callback(
    callback_context,
    llm_response
):

    print("\n--- AFTER MODEL ---")
    print("Model finished generating a response.")

    return None


# =========================================================
# BEFORE TOOL CALLBACK
# =========================================================

def before_tool_callback(
    callback_context,
    tool,
    tool_args
):

    print("\n--- BEFORE TOOL ---")

    # Display the tool being called
    print("Tool:", tool.name)

    # Display the arguments
    print("Arguments:", tool_args)

    return None


# =========================================================
# AFTER TOOL CALLBACK
# =========================================================

def after_tool_callback(
    callback_context,
    tool,
    tool_args,
    tool_response
):

    print("\n--- AFTER TOOL ---")

    # Display the tool result
    print("Tool result:", tool_response)

    return None


# =========================================================
# AGENT
# =========================================================

root_agent = Agent(
    model="gemini-2.0-flash",

    name="weather_agent",

    instruction="""
    You are a helpful weather assistant.

    Use the get_weather tool when the user
    asks about the weather.
    """,

    # Register the tool
    tools=[get_weather],

    # Agent callbacks
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,

    # Model callbacks
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,

    # Tool callbacks
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)