from google.adk.events import Event
from google.genai import types


# Create an event
event = Event(
    author="user",
    content=types.Content(
        role="user",
        parts=[
            types.Part(text="Hello ADK!")
        ],
    ),
)


# Print event details
print("Author:", event.author)
print("Content:", event.content)