import requests
import re
from bs4 import BeautifulSoup

PRICE_REGEX = re.compile( #matches patterns for price per week
    r"(?:from\s*)?\$?\s*(\d{1,3}(?:\.\d{1,2})?)\s*(?:per\s*week|\/\s*week|pw)\b",
    re.IGNORECASE
)

def scrape_price_per_week(url: str) -> str:
    if not url:
        return "N/A"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            }
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[PRICE SCRAPER ERROR] {url} -> {e}")
        return "N/A"

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    match = PRICE_REGEX.search(text)
    if match:
        return f"${match.group(1)} pw"

    return "N/A"