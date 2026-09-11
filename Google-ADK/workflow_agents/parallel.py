from google.adk.agents import Agent
from google.adk.agents import ParallelAgent


weather_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    instruction="Find the weather information."
)


flight_agent = Agent(
    model="gemini-2.0-flash",
    name="flight_agent",
    instruction="Find flight information."
)


hotel_agent = Agent(
    model="gemini-2.0-flash",
    name="hotel_agent",
    instruction="Find hotel information."
)


root_agent = ParallelAgent(
    name="travel_research",
    sub_agents=[
        weather_agent,
        flight_agent,
        hotel_agent
    ]
)