#model context protocol

# Import ADK Agent
from google.adk.agents import Agent

# Import MCP toolset
from google.adk.tools.mcp_tool import (
    McpToolset,
    StreamableHTTPConnectionParams,
)


# Connect to an MCP server
mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        # MCP server URL
        url="https://example.com/mcp",
    )
)


# Create ADK agent
root_agent = Agent(
    # Model used by the agent
    model="gemini-2.0-flash",

    # Agent name
    name="mcp_agent",

    # Agent instructions
    instruction="Use the available MCP tools when needed.",

    # Give MCP tools to the agent
    tools=[mcp_tools],
)