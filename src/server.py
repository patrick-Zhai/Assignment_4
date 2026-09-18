from mcp.server import MCPServer

from openalex_client import search_works

from openai_client import analyze_paper_set


# Based on the official MCP Python SDK quickstart:
# https://github.com/modelcontextprotocol/python-sdk
# mcp dev src/server.py

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


@mcp.tool()
def analyze_papers(
    papers: list[dict],
    research_question: str,
) -> str:
    """
    Analyze academic paper metadata in relation to a research question.

    Args:
        papers: A list of paper metadata, typically returned by search_papers.
        research_question: The research question guiding the analysis.

    Returns:
        A synthesized analysis based only on the supplied paper metadata.
    """

    if not papers:
        raise ValueError("At least one paper is required for analysis.")

    if len(papers) > 10:
        raise ValueError("A maximum of 10 papers can be analyzed at once.")

    research_question = research_question.strip()

    if not research_question:
        raise ValueError("Research question cannot be empty.")

    if len(research_question) > 500:
        raise ValueError(
            "Research question must be 500 characters or fewer."
        )

    return analyze_paper_set(
        papers=papers,
        research_question=research_question,
    )


@mcp.prompt()
def literature_review(
    topic: str,
    research_question: str,
) -> str:
    """
    Create a structured prompt for conducting a small academic literature review.
    """

    return f"""
Conduct a focused academic literature review on the following topic:

Topic:
{topic}

Research question:
{research_question}

Use the available MCP tools as follows:

1. Use search_papers to find relevant academic papers.
2. Review the returned paper metadata and select the most relevant papers.
3. Use analyze_papers to compare and synthesize the selected papers.
4. Clearly distinguish between:
   - information directly supported by the retrieved metadata, and
   - interpretations or limitations caused by missing abstracts or full text.
5. Do not invent methods, findings, datasets, or conclusions that are not
   available in the retrieved information.

Your final response should contain:

- A short overview of the literature
- Main themes
- Important similarities and differences
- Papers most relevant to the research question
- Limitations of the available evidence
- A short conclusion
"""