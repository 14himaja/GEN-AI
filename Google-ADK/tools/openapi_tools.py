# Import ADK Agent
from google.adk.agents import Agent

# Import OpenAPI toolset
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset


# Describe the API using OpenAPI
openapi_spec = """
openapi: 3.0.0
info:
  title: Weather API
  version: 1.0.0

paths:
  /weather:
    get:
      operationId: getWeather
      summary: Get weather for a city
      parameters:
        - name: city
          in: query
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Weather information
"""


# Create tools from the OpenAPI specification
openapi_tools = OpenAPIToolset(
    spec_str=openapi_spec
)


# Create the ADK agent
root_agent = Agent(
    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent name
    name="weather_agent",

    # Agent instructions
    instruction="Use the weather API tool when the user asks about weather.",

    # Give API tools to the agent
    tools=[openapi_tools],
)