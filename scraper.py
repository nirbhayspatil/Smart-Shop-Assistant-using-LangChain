"""
Website scraper — fetches a URL and extracts readable text content.

Strips HTML tags, scripts, styles, and common non-content elements
so the summarizer receives clean plain text.
"""

import requests
from bs4 import BeautifulSoup


def get_website_text(url):
    """
    Download a webpage and return its main text content.

    Args:
        url: The full URL to fetch (e.g. https://example.com).

    Returns:
        Clean plain text on success, or an error message string on failure.
    """
    # Mimic a real browser so sites are less likely to block the request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        # Fetch the page HTML (10s timeout to avoid hanging on slow sites)
        response = requests.get(url, headers=headers, timeout=10)

        # Raise an error if the server returned 4xx/5xx (e.g. 404, 403)
        response.raise_for_status()

        # Parse HTML into a navigable tree
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that aren't useful for summarization
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Pull all visible text and collapse extra blank lines
        raw_text = soup.get_text(separator="\n")
        clean_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        final_text = "\n".join(clean_lines)

        return final_text

    except requests.exceptions.RequestException as e:
        # Return a readable error instead of crashing the app
        return f"An error occurred while fetching the website: {e}"
