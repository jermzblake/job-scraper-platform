from django.utils import timezone

from jobs.models import Company, ScrapeRun
from scrapers import ScrapeTarget, scrape


def run_scrape(*, company_id: int | None = None, source: str | None = None) -> int:
    """
    Orchestrate a scrape run: fetch, parse, and persist jobs.

    Returns the ScrapeRun primary key.
    """
    company = Company.objects.filter(pk=company_id).first() if company_id else None
    scrape_source = source or "default"

    scrape_run = ScrapeRun.objects.create(
        company=company,
        source=scrape_source,
        status=ScrapeRun.Status.RUNNING,
    )

    try:
        if company is None:
            raise NotImplementedError("Bulk scrape across all companies is not implemented yet.")

        result = scrape(
            ScrapeTarget(
                source=scrape_source,
                url=company.careers_url or company.website,
            )
        )

        if not result.ok:
            scrape_run.status = ScrapeRun.Status.FAILED
            scrape_run.error_message = result.error or "Unknown scrape error"
        else:
            scrape_run.jobs_found = len(result.jobs)
            scrape_run.status = ScrapeRun.Status.SUCCESS
    except NotImplementedError as exc:
        scrape_run.status = ScrapeRun.Status.FAILED
        scrape_run.error_message = str(exc)
    finally:
        scrape_run.finished_at = timezone.now()
        scrape_run.save(
            update_fields=[
                "jobs_found",
                "jobs_created",
                "jobs_updated",
                "status",
                "error_message",
                "finished_at",
            ]
        )

    return scrape_run.pk
