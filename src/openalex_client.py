import os

import httpx
from dotenv import load_dotenv


# OpenAlex API documentation:
# https://docs.openalex.org/

load_dotenv()

BASE_URL = "https://api.openalex.org"
API_KEY = os.getenv("OPENALEX_API_KEY")


def search_works(query: str, limit: int = 5) -> list[dict]:
    """Search OpenAlex for academic papers matching a query."""

    params = {
        "search": query,
        "per-page": limit,
    }

    if API_KEY:
        params["api_key"] = API_KEY

    response = httpx.get(
        f"{BASE_URL}/works",
        params=params,
        timeout=10.0,
    )

    response.raise_for_status()
    data = response.json()

    results = []

    for work in data.get("results", []):
        authors = [
            authorship.get("author", {}).get("display_name", "")
            for authorship in work.get("authorships", [])
        ]

        results.append(
            {
                "id": work.get("id"),
                "title": work.get("title"),
                "year": work.get("publication_year"),
                "authors": authors,
                "doi": work.get("doi"),
                "cited_by_count": work.get("cited_by_count"),
            }
        )

    return results