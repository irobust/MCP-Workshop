import asyncio

from fastmcp import FastMCP

from prompts import prompts_server
from resources import resources_server
from tools import tools_server

mcp = FastMCP("Corporate Assistant")


async def setup():
    await mcp.import_server(resources_server)
    await mcp.import_server(tools_server)
    await mcp.import_server(prompts_server)


if __name__ == "__main__":
    asyncio.run(setup())
    mcp.run(transport="http", port=8000)

