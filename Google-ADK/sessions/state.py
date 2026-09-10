###  STATE
import asyncio

# Import session service
from google.adk.sessions import InMemorySessionService


async def main():

    # Create session service
    session_service = InMemorySessionService()

    # Create a session with initial state
    session = await session_service.create_session(
        app_name="my_app",
        user_id="user_1",
        session_id="session_1",
        state={
            "name": "Himaja",
            "learning": "ADK"
        }
    )

    # Read values from state
    print("Name:", session.state["name"])
    print("Learning:", session.state["learning"])


# Run the program
asyncio.run(main())



## state updateeee
import asyncio

# Import session service
from google.adk.sessions import InMemorySessionService


async def main():

    # Create session service
    session_service = InMemorySessionService()

    # Create session
    session = await session_service.create_session(
        app_name="my_app",
        user_id="user_1",
        session_id="session_1",
        state={
            "name": "Himaja"
        }
    )

    # Update state directly
    session.state["goal"] = "Learn ADK"

    # Read updated state
    print("Name:", session.state["name"])
    print("Goal:", session.state["goal"])


# Run the program
asyncio.run(main())