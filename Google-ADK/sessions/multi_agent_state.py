import asyncio

# Import ADK agents
from google.adk.agents import Agent

# Import session service
from google.adk.sessions import InMemorySessionService


# Create first specialist agent
agent_a = Agent(
    model="gemini-2.0-flash",
    name="agent_a",
    instruction="Help with student information.",
)


# Create second specialist agent
agent_b = Agent(
    model="gemini-2.0-flash",
    name="agent_b",
    instruction="Help with learning information.",
)


# Create the main agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="main_agent",
    instruction="Coordinate the specialist agents.",
    sub_agents=[agent_a, agent_b],
)


async def main():

    # Create session service
    session_service = InMemorySessionService()

    # Create shared session state
    session = await session_service.create_session(
        app_name="student_app",
        user_id="user_1",
        session_id="session_1",
        state={
            "student_name": "Himaja",
            "course": "ADK",
        },
    )

    # Read state
    print("Student:", session.state["student_name"])
    print("Course:", session.state["course"])


# Run the program
asyncio.run(main())