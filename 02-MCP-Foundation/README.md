# MCP Foundation
## Step 1: Creating Core MCP Server
Now it's time to bring your server to life by setting up the core application object in server.py.

Step 1: Import the FastMCP class from the fastmcp library using from fastmcp import FastMCP.
```python
from fastmcp import FastMCP
```

Step 2: Create an instance of the FastMCP class. Pass a string name for your server (e.g., "Corporate Assistant") as the first argument. Make sure to assign this new object to a variable named mcp.
```python
mcp = FastMCP("Corporate Assistant")
```

Step 3: Go to the end of the file and add the special Python entry point block.

Step 4: Inside this block, call the run() method on your mcp instance: mcp.run(). This will start the FastMCP server.

```python
if __name__ == "__main__":
    mcp.run()
```

## Step 2: Implementing MCP Resources
### Task 1
Time to give your LLM some context!

You'll start by creating a 'static resource' that provides a list of company holidays. You'll do this in the resources.py file.

1. First, define a new Python function named company_holidays. This function won't need any arguments.
1. Just above your new function, add the `@resources_server.resource()` decorator. The decorator requires a URI as its first argument (a string that uniquely identifies the resource).
    * For this static resource, use the URI `corporate://holidays/2025`.
    * You can also add a description parameter, for example: 
        ```
        description="Provides a list of official company holidays for the year 2025."
        ```
1. Inside the function, return a Python list containing a few dates as strings.
    * For example, you could include dates for New Year's Day and Christmas: `["2025-01-01", "2025-12-25"]`

### Task 2
Now you'll create a dynamic resource that can look up employee details on demand. You'll continue working in `resources.py`.

1. Create a new function called get_employee_details. This function should accept a single argument, employee_id, with a str type hint.
1. Decorate the function with @resources_server.resource() to register it. For dynamic resources, the URI should include a placeholder for the parameter.
    * Use the URI `corporate://employees/{employee_id}` (the {employee_id} will be replaced with the actual value when the resource is accessed).
    * You can also add a description parameter, for example: 
        ```
        description="Fetches employee details for a given employee ID."
        ```
1. Inside the function, use the provided employee_id to find the corresponding employee in the employees dictionary from data.py.
    * Make sure to import employees at the top of the file.
1. Handle cases where the ID isn't found. The `.get()` dictionary method is perfect for this—it can return a default value, like a dictionary with an 'error' message, if the employee ID doesn't exist.

## Step 3 Implementing MCP Prompt
### Task 1
You'll help your LLM write consistent emails by creating a prompt template. This will be a reusable structure for generating welcome messages. You'll be working in `prompts.py`.

1. Define a new function called `generate_welcome_email`. It doesn't need any arguments.
1. Add the `@prompts_server.prompt()` decorator above the function to register it as a prompt.
1. Inside the function, return a multi-line string (using triple quotes) that serves as the welcome email template. Make sure to include placeholders like `{new_hire_name}` and `{start_date}` so the LLM knows where to insert the specific details.

### Task 2
You'll build a more advanced prompt that can be customized on the fly. You'll create a prompt that generates a project status update using details you provide. Stay in `prompts.py` for this.

1. Define a function named `project_status_update`.
1. This function should accept two arguments:
    * `project_name` with a `str` type hint
    * `progress` with an `int` type hint
1. Add the `@prompts_server.prompt()` decorator above the function to register it.
1. Inside the function, use a Python f-string to construct and return a message. The message should dynamically include the `project_name` and `progress` values passed into the function.

## Step 4 Implementing MCP Tools
### Task 1
Now for the really powerful part — tools! These are functions the LLM can decide to run to perform actions.

You'll start with a simple one in `tools.py`.

1. Define a new function called `list_meeting_rooms`. It doesn't need any arguments.
1. Decorate this function with `@tools_server.tool()` to register it as a tool.
1. Inside the function, return a list of available meeting rooms. For example, you could return a list like:
    ```
    ['Conference Room A', 'Conference Room B', 'Board Room']
    ```
### Task 2
Next, you'll create a more useful tool that can take arguments. You'll build a function that allows the LLM to send an email to a specific recipient. You'll get this done in `tools.py`.

1. Define a new function named send_email.
1. This function must accept three arguments with type hints:
    * recipient: str
    * subject: str
    * body: str
1. Register it as a tool by adding the `@tools_server.tool()` decorator.
1. For this step, the function's job is to simply confirm that the email was sent. Just have it return a dictionary confirming the success, like: 
```
{'status': 'sent', 'recipient': recipient, 'subject': subject}
```

### Task 3
Good tools should handle bad inputs gracefully. You'll add some error handling to your `send_email` tool to make it more robust. You'll add basic email validation to ensure the recipient has a valid email format.

1. Go back to your `send_email` function in `tools.py`.
1. At the very top of the function, add a condition that checks if the `recipient` contains the @ symbol (a basic email validation).
1. If the condition is false (meaning no @ symbol), use the `raise` keyword to create a `ValueError` with the specific message: 
    ```
    "Invalid email address: recipient must contain '@' symbol."
    ```
## Step 5: Final Validation
You've built all your components, but there's one final, crucial step: making sure the main application knows about them!

You need to import the server instances from each module and combine them with the main `mcp` instance. You'll connect everything together in `server.py`:

1. Open the `server.py` file.
1. Find the line where you created the `mcp` instance.
1. Import the server instances: 
    ```
    from resources import resources_server
    from prompts import prompts_server
    from tools import tools_server
    ```
1. Create an async `setup()` function that uses `await mcp.import_server()` to register each server instance.
1. In the 
```
if __name__ == '__main__':
```
block, call `asyncio.run(setup())` before calling `mcp.run()`.

## Running
### Step 1: Start the Server
In your first terminal, navigate to the workspace root directory and start the server:

```bash
python3 server.py
```

The server will start and listen on `http://localhost:8000/mcp` by default.

### Step 2: Run the Client
In the second terminal, navigate to the same workspace root directory and run the client:

```bash
python3 client.py
```

The client will connect to your server and test all the components you've built:

* __Resources__: Tests the company_holidays and get_employee_details resources
* __Prompts__: Tests the generate_welcome_email and project_status_update prompts
* __Tools__: Tests the list_meeting_rooms and send_email tools
* __Error Handling__: Verifies that the send_email tool properly handles invalid email addresses

#### Expected Output
You should see output like:
* Lists of available resources, prompts, and tools
* Company holidays data
* Employee details
* Email templates
* Meeting room lists
* Email sending confirmations
* Error handling verification for invalid emails

If everything is working correctly, you'll see "All tests completed successfully!" at the end.