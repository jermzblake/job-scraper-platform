from django.core.management.base import BaseCommand

from jobs.tasks import scrape_all, scrape_company


class Command(BaseCommand):
    help = "Scrape job listings from configured sources."

    def add_arguments(self, parser):
        parser.add_argument(
            "--company",
            type=int,
            help="Company primary key to scrape.",
        )
        parser.add_argument(
            "--source",
            type=str,
            # default='https://hiringcafe.com/'
            default='https://mock-jobs-board.com',
            help="Scraper/parser source identifier (e.g. greenhouse, lever).",
        )

    def handle(self, *args, **options):
        company_id = options.get("company")
        source = options.get("source")
        
        self.stdout.write(self.style.WARNING(f"Initializing scraping engine sequence for: {source}"))

        if company_id:
            scrape_run_id = scrape_company(company_id, source=source)
            self.stdout.write(
                self.style.SUCCESS(f"Scrape run {scrape_run_id} finished for company {company_id}.")
            )
            return

        scrape_run_id = scrape_all(source=source)
        self.stdout.write(self.style.SUCCESS(f"Scrape run {scrape_run_id} finished for all companies."))
