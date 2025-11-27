# TODO: Task 6.1 - Import the server instances and combine them with the main mcp instance

# Task 2.1 step 1 completed: Import the FastMCP class from the fastmcp library
from fastmcp import FastMCP

# Task 2.1 step 2 completed: Create an instance of the FastMCP class and assign it to a variable named 'mcp'
mcp = FastMCP("Corporate Assistant")

# Task 2.2 step 1 completed: Add the special Python entry point block: if __name__ == "__main__":
# Task 2.2 step 2 completed: Inside the entry point block, call the run() method on your mcp instance
if __name__ == "__main__":
    mcp.run()
