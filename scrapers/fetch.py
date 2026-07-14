"""HTTP fetch helpers for scrapers."""

from __future__ import annotations

import logging

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


class FetchError(Exception):
    """Raised when an HTTP fetch fails."""


def fetch_url(
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    headers: dict[str, str] | None = None,
) -> str:
    """
    Fetch URL contents as text.

    Raises FetchError on network failures, timeouts, or non-success HTTP status.
    """
    request_headers = {**DEFAULT_HEADERS, **(headers or {})}
    try:
        response = requests.get(url, headers=request_headers, timeout=timeout)
        response.raise_for_status()
        if not response.encoding:
            response.encoding = response.apparent_encoding or "utf-8"
        return response.text
    except requests.RequestException as exc:
        logger.error("Failed to fetch %s: %s", url, exc)
        raise FetchError(str(exc)) from exc
