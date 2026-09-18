from openai import OpenAI
from dotenv import load_dotenv


# OpenAI Python SDK / Responses API:
# https://developers.openai.com/api/docs/libraries

load_dotenv()

client = OpenAI()


def analyze_paper_set(
    papers: list[dict],
    research_question: str,
) -> str:
    """
    Analyze a set of academic paper metadata against a research question.
    """

    if not papers:
        raise ValueError("At least one paper is required for analysis.")

    if not research_question.strip():
        raise ValueError("Research question cannot be empty.")

    prompt = f"""
You are assisting with academic research.

Research question:
{research_question}

Paper metadata:
{papers}

Analyze ONLY the information provided above.

Please provide:
1. Main themes across the papers
2. Important similarities
3. Important differences
4. Which papers appear most relevant to the research question
5. Important limitations of this analysis

Do not invent paper contents that are not present in the metadata.
Be explicit when the provided metadata is insufficient.
"""

    response = client.responses.create(
        model="gpt-6-astra",
        input=prompt,
    )

    return response.output_text