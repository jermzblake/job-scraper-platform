from dataclasses import dataclass

from scrapers.fetch import FetchError, fetch_url
from scrapers.parsers import ParsedJob, parse_jobs


@dataclass(frozen=True)
class ScrapeTarget:
    source: str
    url: str


@dataclass
class ScrapeResult:
    jobs: list[ParsedJob]
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


def scrape(target: ScrapeTarget) -> ScrapeResult:
    """Fetch and parse job listings for a single target URL."""
    try:
        raw_content = fetch_url(target.url)
        jobs = parse_jobs(target.source, raw_content)
    except (FetchError, NotImplementedError) as exc:
        return ScrapeResult(jobs=[], error=str(exc))

    return ScrapeResult(jobs=jobs)
