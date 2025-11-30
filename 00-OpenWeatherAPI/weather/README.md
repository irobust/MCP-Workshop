# Open Meteo Weather API
## Create MCP Server
1. Init Project
    ```bash
    $ uv init weather
    ```
1. Create Virtual Environment
    ```bash
    $ cd weather
    $ uv venv
    ```
1. Activate Virtual Environment
    ```bash
    $ source .venv/bin/activate
    ```
    or Windows
    ```powershell
    > .venv\Scripts\activate
    ```
1. Install FastMCP
    ```bash
    $ uv add fastmcp httpx
    ```
1. Create MCP Server(`server.py`)
1. Run Hello in Development Mode
    ```bash
    $ fastmcp dev server.py
    ```
1. Add Configuration to Clude Developer Settings
    ```bash
    "weather-forecast": {
        "command": "/opt/homebrew/bin/uv",
        "args": [
            "--directory",
            "/Users/phanupong/Documents/Workshop/MCP-Workshop-1/00-OpenWeatherAPI/weather",
            "run",
            "server.py"
        ]
    }
    ```