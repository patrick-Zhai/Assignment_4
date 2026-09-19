from mcp.server import MCPServer

from openalex_client import search_works

from openai_client import analyze_paper_set

from security import (
sanitize_search_query,
validate_paper_limit,
sanitize_research_question,
validate_paper_list,
)


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
    """

    safe_query = sanitize_search_query(query)
    safe_limit = validate_paper_limit(limit)

    return search_works(
        query=safe_query,
        limit=safe_limit,
    )


@mcp.tool()
def analyze_papers(
    papers: list[dict],
    research_question: str,
) -> str:
    """
    Analyze academic paper metadata in relation to a research question.
    """

    safe_papers = validate_paper_list(papers)
    safe_question = sanitize_research_question(research_question)

    return analyze_paper_set(
        papers=safe_papers,
        research_question=safe_question,
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