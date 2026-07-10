"""HTTP fetch helpers for scrapers."""

import urllib.error
import urllib.request


class FetchError(Exception):
    pass


def fetch_url(url: str, *, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "job-scraper-platform/0.1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode(response.headers.get_content_charset() or "utf-8")
    except urllib.error.URLError as exc:
        raise FetchError(str(exc)) from exc
