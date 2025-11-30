from .models import Tool, ToolParameter

# Task 4.1 - Create the get_weather tool function
def get_weather(location: str) -> str:
        """Gets the current weather for a specified location."""
        return f"The weather in {location} is sunny."

# Task 4.2 - Define the Tool Schema for get_weather
GET_WEATHER_TOOL = Tool(
    name="get_weather",
    description="Gets the current weather for a specified location.",
    parameters=[
        ToolParameter(name="location", type="string")
    ]
)
