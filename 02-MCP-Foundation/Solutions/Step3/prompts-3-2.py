from fastmcp import FastMCP

prompts_server = FastMCP(name="CorporatePrompts")


@prompts_server.prompt(description="Generates a welcome email for a new employee.")
def generate_welcome_email():
    """Returns a template for a new hire welcome email."""
    return """Subject: Welcome to the team!

Hi {new_hire_name},

We are thrilled to have you join us. Your official start date is {start_date}.
We look forward to working with you!

Best,
HR Team"""


@prompts_server.prompt(description="Creates a formatted project status update.")
def project_status_update(project_name: str, progress: int):
    """Generates a status update for a project with its current progress."""
    return f"""**Status Update**

Project: {project_name}
Current Progress: {progress}%

Next steps: [LLM should fill this in]"""

