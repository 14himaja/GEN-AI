# SESSIONS

import asyncio

# Import session service
from google.adk.sessions import InMemorySessionService


async def main():

    # Create session service
    session_service = InMemorySessionService()

    # Create a session
    session = await session_service.create_session(
        app_name="my_app",
        user_id="user_1",
        session_id="session_1",
    )

    # Print session details
    print("Session created!")
    print("App:", session.app_name)
    print("User:", session.user_id)
    print("Session ID:", session.id)


# Run the program
asyncio.run(main())

