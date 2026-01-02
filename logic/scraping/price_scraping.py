import requests
import re
from bs4 import BeautifulSoup

PRICE_REGEX = re.compile( #matches patterns for price per week
    r"\$?\s?(\d{1,3})(?:\.\d{2})?\s?(?:per\s?week|\/week|pw)",
    re.IGNORECASE
)

def scrape_price_per_week(url: str) -> str:
    if not url:
        return "N/A"

    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        response.raise_for_status()
    except requests.RequestException:
        return "N/A"

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    match = PRICE_REGEX.search(text)
    if match:
        return f"${match.group(1)} pw"

    return "N/A"