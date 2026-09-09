# Import required modules
import datetime
from zoneinfo import ZoneInfo

# Import ADK agent
from google.adk.agents import Agent, LlmAgent


# Weather tool
def get_weather(city: str) -> dict:
    """Get weather information for a city."""

    # Check for New York
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees "
                "Celsius (77 degrees Fahrenheit)."
            ),
        }

    # Return error for other cities
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


# Current time tool
def get_current_time(city: str) -> dict:
    """Get the current time for a city."""

    # Set timezone for New York
    if city.lower() == "new york":
        tz_identifier = "America/New_York"

    # Return error for other cities
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    # Get current time
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)

    # Create time report
    report = (
        f"The current time in {city} is "
        f"{now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    )

    return {
        "status": "success",
        "report": report,
    }


# Create the main ADK agent
root_agent = LlmAgent(
    # Agent name
    name="weather_time_agent",

    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent purpose
    description="Agent to answer questions about the time and weather in a city.",

    # Agent instructions
    instruction=(
        "You are a helpful agent who can answer user questions "
        "about the time and weather in a city."
    ),

    # Give tools to the agent
    tools=[get_weather, get_current_time],
)