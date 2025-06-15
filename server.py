from fastmcp import FastMCP, Context

mcp = FastMCP("Web Search MCP Server")

@mcp.tool
async def search_web(search_term: str, ctx: Context):
    await ctx.info(f"Searching for: {search_term} on Web")

    return {"some result", "result 2", "result 3"}

mcp.run(transport="streamable-http", host = "127.0.0.1", port = 8000, path = "/mcp")
