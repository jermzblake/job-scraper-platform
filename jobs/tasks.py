"""
Background job entry points.

Wire these to Celery when ready, e.g.:

    from celery import shared_task

    @shared_task
    def scrape_company(company_id: int, source: str | None = None) -> int:
        ...
"""

from jobs.services.scrapers import run_scrape


def scrape_company(company_id: int, source: str | None = None) -> int:
    """Scrape jobs for a single company. Returns the ScrapeRun pk."""
    return run_scrape(company_id=company_id, source=source)


def scrape_all(source: str | None = None) -> int:
    """Scrape jobs for all companies. Returns the ScrapeRun pk."""
    return run_scrape(source=source)
