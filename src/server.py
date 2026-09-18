from mcp.server import MCPServer

from openalex_client import search_works


# Based on the official MCP Python SDK quickstart:
# https://github.com/modelcontextprotocol/python-sdk

mcp = MCPServer("Academic Research Assistant")


@mcp.tool()
def hello(name: str) -> str:
    """Return a simple greeting to verify that the MCP server works."""
    return f"Hello, {name}! The MCP server is working."


@mcp.tool()
def search_papers(query: str, limit: int = 5) -> list[dict]:
    """
    Search for academic papers related to a research topic.

    Args:
        query: Research topic or keywords.
        limit: Number of papers to return, between 1 and 10.
    """

    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be empty.")

    if len(query) > 200:
        raise ValueError("Search query must be 200 characters or fewer.")

    if limit < 1 or limit > 10:
        raise ValueError("Limit must be between 1 and 10.")

    return search_works(query=query, limit=limit)