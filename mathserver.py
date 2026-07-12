from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int, b:int) -> int:
    """Adds two numbers"""
    return a+b

@mcp.tool()
def multiple(a:int, b:int)-> int:
    """Multiplies two numbers"""
    return a*b

# The transport = "stdio" argument tells the server to:
# use standard input / output (stdin and stdout) to recieve and respond to the tool functional calls
if __name__ == "__main__":
    mcp.run(transport="stdio")


