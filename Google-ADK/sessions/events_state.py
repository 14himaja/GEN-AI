import asyncio

# Import session service
from google.adk.sessions import InMemorySessionService

# Import Event
from google.adk.events import Event

# Import EventActions
from google.adk.events import EventActions


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
        },
    )

    # Create state update action
    actions = EventActions(
        state_delta={
            "course": "ADK"
        }
    )

    # Create an event with the state update
    event = Event(
        author="agent",
        actions=actions,
    )

    # Save the event
    await session_service.append_event(
        session=session,
        event=event,
    )

    # Read updated state
    print("Name:", session.state["name"])
    print("Course:", session.state["course"])


# Run the program
asyncio.run(main())