"""
Example client for connecting to the Corporate Assistant FastMCP server.

This demonstrates how to connect to and interact with the MCP server using the FastMCP Client.
The server must be running before you run this client.

Usage:
    # First, start the server in one terminal:
    # python server.py

    # Then, in another terminal, run the client:
    python client.py
"""

import asyncio
import sys

from fastmcp import Client


async def test_server():
    """Test the Corporate Assistant MCP server."""
    # Connect to the server via HTTP
    # The server must be running and accessible at this URL
    # Default FastMCP HTTP endpoint is http://localhost:8000/mcp
    client = Client("http://localhost:8000/mcp")

    try:
        async with client:
            print("Connected to Corporate Assistant MCP server!\n")

            # Test listing resources
            print("=== Testing Resources ===")
            resources = await client.list_resources()
            print(f"Available resources: {[r.name for r in resources]}\n")

            # Test reading a resource
            if any(r.name == "company_holidays" for r in resources):
                holidays = await client.read_resource("corporate://holidays/2025")
                print(f"Company holidays: {holidays}\n")

            # Test getting employee details
            if any(r.name == "get_employee_details" for r in resources):
                employee = await client.read_resource(
                    "corporate://employees/{employee_id}", {"employee_id": "U123"}
                )
                print(f"Employee details: {employee}\n")

            # Test listing prompts
            print("=== Testing Prompts ===")
            prompts = await client.list_prompts()
            print(f"Available prompts: {[p.name for p in prompts]}\n")

            # Test getting a prompt
            if any(p.name == "generate_welcome_email" for p in prompts):
                email_template = await client.get_prompt("generate_welcome_email", {})
                print(f"Welcome email template:\n{email_template}\n")

            # Test getting a parameterized prompt
            if any(p.name == "project_status_update" for p in prompts):
                status = await client.get_prompt(
                    "project_status_update",
                    {"project_name": "Q4 Launch", "progress": 75},
                )
                print(f"Project status update:\n{status}\n")

            # Test listing tools
            print("=== Testing Tools ===")
            tools = await client.list_tools()
            print(f"Available tools: {[t.name for t in tools]}\n")

            # Test calling a tool
            if any(t.name == "list_meeting_rooms" for t in tools):
                rooms = await client.call_tool("list_meeting_rooms", {})
                print(f"Meeting rooms: {rooms}\n")

            # Test sending an email (with valid email)
            if any(t.name == "send_email" for t in tools):
                result = await client.call_tool(
                    "send_email",
                    {
                        "recipient": "alice@company.com",
                        "subject": "Test Email",
                        "body": "This is a test email from the MCP client.",
                    },
                )
                print(f"Email sent: {result}\n")

            # Test error handling (invalid email)
            print("=== Testing Error Handling ===")
            try:
                await client.call_tool(
                    "send_email",
                    {
                        "recipient": "invalid-email",
                        "subject": "Test",
                        "body": "This should fail.",
                    },
                )
                print("ERROR: Should have raised ValueError for invalid email!")
            except Exception as e:
                print(f"Correctly caught error for invalid email: {e}\n")

            print("All tests completed successfully!")

    except Exception as e:
        print(f"Error connecting to server: {e}")
        print("\nMake sure the server is running first!")
        print("\nTo start the server, run in one terminal:")
        print("  python server.py")
        print("\nOr if you want to use HTTP transport, update server.py to use:")
        print("  mcp.run(transport='http', host='0.0.0.0', port=8000)")
        print("\nThen run this client in another terminal.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_server())
