import re


MAX_QUERY_LENGTH = 200
MAX_RESEARCH_QUESTION_LENGTH = 500
MAX_PAPERS = 10


def sanitize_search_query(query: str) -> str:
    """
    Validate and sanitize a paper search query.
    """

    if not isinstance(query, str):
        raise ValueError("Search query must be a string.")

    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be empty.")

    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(
            f"Search query must be {MAX_QUERY_LENGTH} characters or fewer."
        )

    # Reject common command / injection control characters.
    dangerous_patterns = [
        r";",
        r"--",
        r"\bDROP\b",
        r"\bDELETE\b",
        r"\bINSERT\b",
        r"\bUPDATE\b",
        r"\bEXEC\b",
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, query, flags=re.IGNORECASE):
            raise ValueError(
                "Search query contains potentially unsafe input."
            )

    return query


def validate_paper_limit(limit: int) -> int:
    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer.")

    if limit < 1 or limit > 10:
        raise ValueError("Limit must be between 1 and 10.")

    return limit


def sanitize_research_question(question: str) -> str:
    if not isinstance(question, str):
        raise ValueError("Research question must be a string.")

    question = question.strip()

    if not question:
        raise ValueError("Research question cannot be empty.")

    if len(question) > MAX_RESEARCH_QUESTION_LENGTH:
        raise ValueError(
            f"Research question must be "
            f"{MAX_RESEARCH_QUESTION_LENGTH} characters or fewer."
        )

    return question


def validate_paper_list(papers: list[dict]) -> list[dict]:
    if not papers:
        raise ValueError("At least one paper is required.")

    if len(papers) > MAX_PAPERS:
        raise ValueError(
            f"A maximum of {MAX_PAPERS} papers can be analyzed at once."
        )

    return papers