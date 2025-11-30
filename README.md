# Model Context Protocol(MCP)
## Using Third-Party MCP Server
- https://github.com/modelcontextprotocol/servers
- https://github.com/mcp
- https://mcp.so/
- https://www.pulsemcp.com/

### Using Time MCP Server
1. Go to Settings
1. Choose `Developer`
1. Edit Config
1. Add MCP Servers
    ```json
    {
    "mcpServers": {
        "time": {
        "command": "uvx",
        "args": ["-q","mcp-server-time","--local-timezone=America/New_York"]
        }
    }
    }
    ```

## Create MCP Server
1. Install UV
    ```bash
    $ pip install uv
    ```
1. Init Project
    ```bash
    $ uv init hello
    ```
1. Create Virtual Environment
    ```bash
    $ cd hello
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
    $ uv add fastmcp
    ```
1. Create MCP Server(`server.py`)
    ```python
    from fastmcp import FastMCP

    mcp = FastMCP("Hello MCP Server")

    @mcp.tool
    def say_hello(name: str) -> str:
        return f"Hello, {name}!"

    if __name__ == "__main__":
        print("🚀 Starting MCP server at http://localhost:8000/mcp")
        mcp.run(transport="http", port=8000)
    ```

1. Run Hello in Development Mode
    ```bash
    $ fastmcp dev server.py
    ```
1. Add Configuration to Clude Developer Settings
    ```bash
    "hello": {
        "command": "/opt/homebrew/bin/uv",
        "args": [
            "--directory",
            "/Users/phanupong/Documents/Workshop/hello",
            "run",
            "server.py"
        ]
    }
    ```

### Debugging MCP Server
1. MCP Inspector
1. Claude Desktop Debugging
    * Click the connection icon to view 
        1. Connected server
        1. Available prompts and resources
    * Click View MCP Server Log when error happen

1. Using Chrome Dev Tools
    * Add `allowDevTools` to Developer Settings
        ```json
        { "allowedDevTools" : true }
        ```
    * Open DevTools: `Command + Option + Shift + i`

### Running Without Virtual Environment
1. Change directory to `hello` folder
1. Run npx to start MCP Inspector
    ```bash
    $ npx @modelcontextprotocol/inspector uv run server.py
    ```
    On MacOs you need to install inspector before
    ```
    $ npm i @modelcontextprotocol/inspector
    ```
