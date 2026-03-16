import json
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from html import unescape
from typing import Iterable, Optional

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

PRICE_CONTAINER_SELECTORS = [
    "[class*='price']",
    "[class*='pricing']",
    "[class*='plan']",
    "[class*='membership']",
    "[class*='offer']",
    "[class*='package']",
    "[class*='tier']",
    "[class*='card']",
    "[id*='price']",
    "[id*='pricing']",
    "[id*='membership']",
]

CARD_HINTS = (
    "price",
    "pricing",
    "membership",
    "memberships",
    "plan",
    "plans",
    "week",
    "weekly",
    "fortnight",
    "fortnightly",
    "month",
    "monthly",
    "join",
)

PRICE_PATTERN = re.compile(
    r"(?P<prefix>from\s+|starting\s+at\s+|only\s+)?"
    r"(?P<currency>\$|nz\$|nzd\s*)?\s*"
    r"(?P<amount>\d{1,4}(?:[.,]\d{1,2})?)"
    r"\s*(?P<suffix>(?:/|per\s+)?(?:wk|week|weekly|fortnight|fortnightly|fn|month|monthly|mo|year|yearly|annum|pa))\b",
    re.IGNORECASE,
)

PRICE_AND_PERIOD_SEPARATE_PATTERN = re.compile(
    r"(?P<prefix>from\s+|starting\s+at\s+|only\s+)?"
    r"(?P<currency>\$|nz\$|nzd\s*)?\s*"
    r"(?P<amount>\d{1,4}(?:[.,]\d{1,2})?)\b"
    r"(?P<middle>.{0,40}?)"
    r"\b(?P<period>wk|week|weekly|fortnight|fortnightly|fn|month|monthly|mo|year|yearly|annum|pa)\b",
    re.IGNORECASE | re.DOTALL,
)

NUMERIC_PRICE_PATTERN = re.compile(r"(?<!\d)(\d{1,4}(?:[.,]\d{1,2})?)(?!\d)")
JSON_PRICE_KEYS = {"price", "amount", "membershipPrice", "weeklyPrice", "startingPrice"}


MIN_WEEKLY_PRICE = Decimal("5")
MAX_WEEKLY_PRICE = Decimal("500")

PRICE_CONTEXT_PATTERN = re.compile(
    r"\b(price|pricing|membership|memberships|join|weekly|week|fortnight|fortnightly|month|monthly|year|yearly|per\s+week|per\s+month|per\s+fortnight|direct\s+debit)\b",
    re.IGNORECASE,
)


def _clean_text(text: str) -> str:
    if not text:
        return ""
    text = unescape(text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _decimal_to_weekly(amount: Decimal, period: str) -> Optional[Decimal]:
    period = period.lower().strip()
    if period in {"wk", "week", "weekly"}:
        return amount
    if period in {"fortnight", "fortnightly", "fn"}:
        return amount / Decimal("2")
    if period in {"month", "monthly", "mo"}:
        return amount * Decimal("12") / Decimal("52")
    if period in {"year", "yearly", "annum", "pa"}:
        return amount / Decimal("52")
    return None


def _format_weekly_price(amount: Decimal) -> str:
    weekly = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if weekly == weekly.to_integral():
        return f"${int(weekly)} pw"
    return f"${weekly.normalize()} pw"


def _normalize_amount(raw_amount: str) -> Optional[Decimal]:
    cleaned = raw_amount.replace(",", "")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def _is_reasonable_weekly_amount(weekly_amount: Decimal) -> bool:
    return MIN_WEEKLY_PRICE <= weekly_amount <= MAX_WEEKLY_PRICE


def _extract_weekly_price_from_text(text: str) -> Optional[str]:
    text = _clean_text(text)
    if not text:
        return None

    if not PRICE_CONTEXT_PATTERN.search(text):
        return None

    candidates = []
    for pattern in (PRICE_PATTERN, PRICE_AND_PERIOD_SEPARATE_PATTERN):
        for match in pattern.finditer(text):
            amount = _normalize_amount(match.group("amount"))
            if amount is None:
                continue
            period = match.groupdict().get("suffix") or match.groupdict().get("period")
            if not period:
                continue
            weekly_amount = _decimal_to_weekly(amount, period)
            if weekly_amount is None or not _is_reasonable_weekly_amount(weekly_amount):
                continue
            candidates.append(weekly_amount)

    if not candidates:
        return None

    return _format_weekly_price(min(candidates))


def _extract_json_values(obj) -> Iterable[str]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                yield from _extract_json_values(value)
            else:
                key_lower = str(key).lower()
                if key in JSON_PRICE_KEYS or key_lower in {k.lower() for k in JSON_PRICE_KEYS}:
                    yield f"{key}: {value}"
                elif isinstance(value, str) and any(hint in value.lower() for hint in CARD_HINTS):
                    yield value
    elif isinstance(obj, list):
        for item in obj:
            yield from _extract_json_values(item)


def _extract_from_script_tags(soup: BeautifulSoup) -> Optional[str]:
    for script in soup.find_all("script"):
        script_text = _clean_text(script.get_text(" ", strip=True) or script.string or "")
        if not script_text:
            continue

        script_type = (script.get("type") or "").lower()
        if "ld+json" not in script_type and not (script_text.startswith("{") or script_text.startswith("[")):
            continue

        try:
            parsed = json.loads(script_text)
            joined = " ".join(_extract_json_values(parsed))
            price = _extract_weekly_price_from_text(joined)
            if price:
                return price
        except Exception:
            continue

    return None


def _extract_from_price_containers(soup: BeautifulSoup) -> Optional[str]:
    seen_texts = set()

    for selector in PRICE_CONTAINER_SELECTORS:
        for node in soup.select(selector):
            text = _clean_text(node.get_text(" ", strip=True))
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            if not any(hint in text.lower() for hint in CARD_HINTS):
                continue
            price = _extract_weekly_price_from_text(text)
            if price:
                return price

    return None


def _extract_from_visible_text(soup: BeautifulSoup) -> Optional[str]:
    visible_soup = BeautifulSoup(str(soup), "html.parser")
    for tag in visible_soup(["style", "noscript", "svg"]):
        tag.decompose()

    text = _clean_text(visible_soup.get_text(" ", strip=True))
    return _extract_weekly_price_from_text(text)


def _fetch_rendered_page_text(url: str) -> Optional[str]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=20000)

            for label in ["pricing", "price", "membership", "memberships", "join"]:
                try:
                    locator = page.get_by_text(label, exact=False)
                    if locator.count() > 0:
                        locator.first.click(timeout=1500)
                        page.wait_for_timeout(500)
                except Exception:
                    pass

            content = page.content()
            browser.close()
            return content
    except Exception as exc:
        print(f"[PRICE SCRAPER PLAYWRIGHT FALLBACK ERROR] {url} -> {exc}")
        return None


def scrape_price_per_week(url: str) -> str:
    if not url:
        return "N/A"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=12, headers=DEFAULT_HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(f"[PRICE SCRAPER ERROR] {url} -> {exc}")
        return "N/A"

    soup = BeautifulSoup(response.text, "html.parser")

    for extractor in (
        _extract_from_price_containers,
        _extract_from_script_tags,
        _extract_from_visible_text,
    ):
        price = extractor(soup)
        if price:
            return price

    rendered_content = _fetch_rendered_page_text(url)
    if rendered_content:
        rendered_soup = BeautifulSoup(rendered_content, "html.parser")
        for extractor in (
            _extract_from_price_containers,
            _extract_from_script_tags,
            _extract_from_visible_text,
        ):
            price = extractor(rendered_soup)
            if price:
                return price

    return "N/A"
