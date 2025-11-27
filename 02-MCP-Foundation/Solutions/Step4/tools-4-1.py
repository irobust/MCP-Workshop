# tools.py
from fastmcp import FastMCP

tools_server = FastMCP(name="CorporateTools")


@tools_server.tool(description="Lists all available meeting rooms in the office.")
def list_meeting_rooms():
    """Returns a list of available meeting rooms."""
    return ["Conference Room A", "Conference Room B", "Board Room", "Focus Room"]


# TODO: Task 5.2 - Create a parameterized tool named 'send_email'


# TODO: Task 5.3 - Add error handling to the 'send_email' tool

