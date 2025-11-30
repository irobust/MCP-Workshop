# Create Simple MCP
## Step 1: Setting Up the Basic Server
In this first task, you'll lay the foundation for the server.

1. Open the `app/main.py` file.
2. Import the FastAPI class from the fastapi library.
    ```python
    from fastapi import FastAPI, HTTPException
    ```
3. Create an instance of the FastAPI application and assign it to a variable named app.
    ```python
    app = FastAPI()
    ```

4. In app/main.py, define a new function named **handle_mcp_request**
    ```python
    async def handle_mcp_request():
        pass
    ```
5. Decorate this function with `@app.post("/mcp")` to register it as an HTTP POST endpoint at the `/mcp` path.

    ```python
    @app.post("/mcp")
    async def handle_mcp_request():
        pass
    ```

For now, leave the function body empty by adding pass. You'll implement the logic in later steps.

## Step 2: Defining MCP Data Structures
An MCP server needs to describe the tools it offers. You'll start by defining the **Pydantic** models for a tool's schema.

1. Open `app/models.py`.
1. Create a **Pydantic** model named ToolParameter that inherits from BaseModel. It should include two fields:
    * name: a str               
    * type: a str (e.g., 'string', 'number')
    ```python
    from pydantic import BaseModel
    from typing import Optional, List, Any, Dict


    class ToolParameter(BaseModel):
        name: str
        type: str


    class Tool(BaseModel):
        name: str
        description: str
        parameters: List[ToolParameter]
    ```

1. Create another model named Tool, which also inherits from BaseModel. It should include three fields:
    * name: a str
    * description: a str
    * parameters: a list of ToolParameter objects

    ```python 
    class ModelContextRequest(BaseModel):
        verb: str
        tool_name: Optional[str] = None
        arguments: Optional[Dict[str, Any]] = None


    class ModelContextResponse(BaseModel):
        tools: Optional[List[Tool]] = None
        result: Optional[Any] = None
    ```
1. In `app/main.py` import `ModelContextRequest` and `ModelContextResponse`

    ```python
    from app.models import ModelContextRequest, ModelContextResponse
    ```
## Step 3: Implement Discovery
### Task 3.1
Now, you can create the first tool that your server will offer, a simple weather tool.

1. Open the `app/tools.py` file.
1. Define a function named get_weather. It should accept one argument: location (a string).
    ```python
    from .models import Tool, ToolParameter


    def get_weather(location: str):
        """Gets the current weather for a specified location."""
    ```

1. Inside the function, return a string indicating the weather. For this lab, you can hardcode the return value.
For example: f"The weather in {location} is sunny."

    ```python
    def get_weather(location: str) -> str:
        """Gets the current weather for a specified location."""
        return f"The weather in {location} is sunny."
    ```
### Task 3.2
A tool needs a corresponding definition that the server can advertise. You'll create this definition using the **Pydantic** models you built earlier.

1. In `app/tools.py`, create an instance of the Tool model for the get_weather function. Assign it to a variable named `GET_WEATHER_TOOL`.
1. Set the name to 'get_weather'
1. Set the description to 'Gets the current weather for a specified location.'
1. Set the parameters to a list containing one ToolParameter instance for the location argument, with its name as 'location' and type as 'string'.
     ```python
    GET_WEATHER_TOOL = Tool(
        name="get_weather",
        description="Gets the current weather for a specified location.",
        parameters=[
            ToolParameter(name="location", type="string")
        ]
    )
    ```
### Task 3.3
With the tool and its schema ready, you can now implement the discovery logic. When an agent sends a discovery request, the server should respond with a list of its available tools.

1. Open app/main.py.
1. Update the `handle_mcp_request` function to accept one argument: request, typed as `ModelContextRequest`.
1. Inside the function, add an if condition to check if request.verb is equal to 'discovery'.
1. If it is, return a `ModelContextResponse` instance where the tools field is a list containing the `GET_WEATHER_TOOL` you defined in the previous step.

    ```python
    from app.tools import GET_WEATHER_TOOL

    app = FastAPI()

    @app.post("/mcp")
    async def handle_mcp_request(request: ModelContextRequest):
        if request.verb == "discovery":
            return ModelContextResponse(tools=[GET_WEATHER_TOOL])
        pass
    ```
## Step 4: Implementing Tools Execution
### Task 4.1
To execute tools dynamically, you need a way to map tool names to their corresponding functions. A dictionary is a great way to create this registry.

1. In app/main.py, create a dictionary named tool_registry.
1. This dictionary should map the tool's name (a string) to its callable function.
1. Add one entry to the registry: the key 'get_weather' should map to the get_weather function you imported from app.tools.
    ```python
    from app.tools import GET_WEATHER_TOOL, get_weather

    tool_registry = {
        "get_weather": get_weather
    }
    ```
### Task 4.2
This is the final piece of the core logic. You'll implement the handler for the execute verb. This involves looking up the tool, calling it with the provided arguments, and returning the result.

1. In `app/main.py`, add an `elif` block to `handle_mcp_request` to check if request.verb is 'execute'.
1. Inside this block, retrieve the function from `tool_registry` using `request.tool_name` as the key.
1. Call the retrieved function, passing in the `request.arguments` using the `**` operator to unpack them as keyword arguments.
1. Store the function's return value.
1. Return a `ModelContextResponse` where the `result` field is set to the value you just stored.

```python
@app.post("/mcp")
async def handle_mcp_request(request: ModelContextRequest):
    if request.verb == "discovery":
        return ModelContextResponse(tools=[GET_WEATHER_TOOL])
    elif request.verb == "execute":
        # TODO: Task 6.1 - Add error handling for unknown tools
        tool_function = tool_registry[request.tool_name]
        arguments = request.arguments or {}
        result = tool_function(**arguments)
        return ModelContextResponse(result=result)

    pass
```

## Step 5: Add Error Handling
## Task 5.1
A robust server should handle bad requests gracefully. What happens if an agent asks for a tool that doesn't exist? You'll add error handling for that case.

1. Open `app/main.py`.
1. Inside the **elif request.verb == 'execute'** block, wrap your tool execution logic in a try...except block.
1. In the try block, attempt to look up the tool in the `tool_registry`.
1. In the except section, `catch a KeyError` (which means the tool was not found) and raise an HTTPException from FastAPI with a status_code of 404 and a detail message like "Tool not found".

    ```python
    @app.post("/mcp", response_model=ModelContextResponse)
    async def handle_mcp_request(request: ModelContextRequest):
        if request.verb == "discovery":
            return ModelContextResponse(tools=[GET_WEATHER_TOOL])
        
        elif request.verb == "execute":
            try:
                tool_function = tool_registry[request.tool_name]
                arguments = request.arguments or {}
                result = tool_function(**arguments)
                return ModelContextResponse(result=result)
            except KeyError:
                raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found.")

        raise HTTPException(status_code=400, detail=f"Unknown verb '{request.verb}'")
    ```