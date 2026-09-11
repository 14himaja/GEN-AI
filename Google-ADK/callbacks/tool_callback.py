from google.adk.agents import Agent


def get_weather(city: str):
    return f"The weather in {city} is sunny."


def before_tool(callback_context, tool, tool_args):

    print("Before tool")
    print("Tool:", tool.name)
    print("Arguments:", tool_args)

    return None


def after_tool(
    callback_context,
    tool,
    tool_args,
    tool_response
):

    print("After tool")
    print("Tool:", tool.name)
    print("Result:", tool_response)

    return None


root_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    instruction="Use the weather tool when the user asks about weather.",

    tools=[get_weather],

    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
)