# tools.py
from fastmcp import FastMCP

tools_server = FastMCP(name="CorporateTools")


@tools_server.tool(description="Lists all available meeting rooms in the office.")
def list_meeting_rooms():
    """Returns a list of available meeting rooms."""
    return ["Conference Room A", "Conference Room B", "Board Room", "Focus Room"]


@tools_server.tool(description="Sends an email to a recipient.")
def send_email(recipient: str, subject: str, body: str):
    """Simulates sending an email to a specific recipient.
    This is a mock tool and does not send real emails.
    """
    if "@" not in recipient:
        raise ValueError("Invalid email address: recipient must contain '@' symbol.")
    
    print(f"EMAIL SENT to {recipient}: {subject}")
    return {"status": "sent", "recipient": recipient, "subject": subject}

