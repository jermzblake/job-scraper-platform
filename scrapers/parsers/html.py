"""Shared BeautifulSoup helpers for HTML-based parsers."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from bs4 import BeautifulSoup, Tag

DEFAULT_FEATURES = "html.parser"


def soup_from_html(html_content: str, *, features: str = DEFAULT_FEATURES) -> BeautifulSoup:
    """Parse HTML into a BeautifulSoup document."""
    return BeautifulSoup(html_content or "", features)


def select_all(root: BeautifulSoup | Tag, selector: str) -> list[Tag]:
    """Return matching tags for a CSS selector."""
    return [el for el in root.select(selector) if isinstance(el, Tag)]


def select_one(root: BeautifulSoup | Tag, selector: str) -> Tag | None:
    """Return the first matching tag for a CSS selector, if any."""
    el = root.select_one(selector)
    return el if isinstance(el, Tag) else None


def text_of(element: Tag | None, *, default: str = "") -> str:
    """Return stripped text for an element, or default when missing."""
    if element is None:
        return default
    return element.get_text(strip=True) or default


def attr_of(element: Tag | None, name: str, *, default: str = "") -> str:
    """Return a string attribute value, or default when missing."""
    if element is None:
        return default

    value: Any = element.get(name)
    if value is None:
        return default
    if isinstance(value, list):
        return str(value[0]) if value else default
    return str(value) or default


def snippet_of(element: Tag | None, *, limit: int = 250) -> str:
    """Return a truncated HTML snippet suitable for metadata storage."""
    if element is None:
        return ""
    return str(element)[:limit]


def iter_cards(html_content: str, card_selector: str) -> Iterable[Tag]:
    """Yield card elements from HTML for a given CSS selector."""
    if not html_content:
        return
    soup = soup_from_html(html_content)
    yield from select_all(soup, card_selector)
