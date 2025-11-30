# Task 2.1 - Import FastAPI
from fastapi import FastAPI,HTTPException
# Task 3.2 - Import request and response models from app.models
from app.models import ModelContextRequest, ModelContextResponse
# Task 4.3 - Import the tool schema from app.tools
# Task 5.1 - Import the tool function from app.tools
from app.tools import GET_WEATHER_TOOL, get_weather


# Task 2.1 - Create the FastAPI app instance
app = FastAPI();

# Task 5.1 - Create the tool_registry dictionary
tool_registry = {
    "get_weather": get_weather
}

# Task 2.2 - Create the /mcp POST endpoint
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
