"""
File Reader Assistant Agent
Demonstrates MCP tools integration with ADK using the filesystem MCP server.

Reference: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Define the folder to allow file access (must be absolute path)
ALLOWED_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "my_files"))

# Create the folder if it doesn't exist
os.makedirs(ALLOWED_PATH, exist_ok=True)

# Create the agent with MCP filesystem tools
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='file_reader_assistant',
    description='Helps users read and explore files using MCP tools.',
    instruction="""
You are a file reader assistant that helps users explore files.
Your capabilities:
 - List files in directories using list_directory
 - Read file contents using read_file

When helping users:
1. Use list_directory to show available files
2. Use read_file to display file contents when asked
3. Describe what you find in a helpful way

Always be clear about which folder you're working with.
""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=[
                        '-y',
                        '@modelcontextprotocol/server-filesystem',
                        ALLOWED_PATH,
                    ],
                ),
            ),
            # Filter to only expose safe, read-only tools
            tool_filter=['list_directory', 'read_file'],
        )
    ],
)


# ###
# """
# Geography Assistant Agent
# Demonstrates ADK's tools parameter with a simple custom function tool.

# Reference: https://google.github.io/adk-docs/agents/llm-agents#tools
# """

# from google.adk.agents import LlmAgent

# # Step 1: Define a tool function
# def get_capital_city(country: str) -> str:
#     """Retrieves the capital city for a specified country.

#     Args:
#         country (str): The name of the country.

#     Returns:
#         str: The capital city name or error message.
#     """
#     # Simulated capital city database
#     capitals = {
#         "france": "Paris",
#         "japan": "Tokyo",
#         "canada": "Ottawa",
#         "germany": "Berlin",
#         "brazil": "Brasília",
#         "australia": "Canberra",
#         "india": "New Delhi",
#         "mexico": "Mexico City"
#     }

#     # Look up the capital
#     return capitals.get(
#         country.lower(),
#         f"Sorry, I don't have information about the capital of {country}."
#     )

# # Step 2: Create agent with the tool
# root_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='geography_assistant',
#     description='Helps users learn about world geography.',
#     instruction="""
#     You are a geography assistant that helps users learn about world capitals.

#     When a user asks about a capital city:
#     1. Use the get_capital_city tool to find the answer
#     2. Provide the information in a friendly, educational way
#     3. You can add interesting facts if you know them

#     If the tool returns an error message, politely tell the user you don't have that information.
#     """,
#     tools=[get_capital_city]  # Provide the function as a tool
# )
