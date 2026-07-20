from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase


class ScrapeJobsCommandTests(SimpleTestCase):
    def test_scrapes_all_companies_with_default_source_when_company_is_omitted(self):
        stdout = StringIO()

        with (
            patch("jobs.management.commands.scrape_jobs.scrape_all", return_value=123) as scrape_all,
            patch("jobs.management.commands.scrape_jobs.scrape_company") as scrape_company,
        ):
            call_command("scrape_jobs", stdout=stdout)

        scrape_all.assert_called_once_with(source="https://mock-jobs-board.com")
        scrape_company.assert_not_called()
        output = stdout.getvalue()
        self.assertIn("Initializing scraping engine sequence for: https://mock-jobs-board.com", output)
        self.assertIn("Scrape run 123 finished for all companies.", output)

    def test_scrapes_single_company_with_custom_source_when_company_is_provided(self):
        stdout = StringIO()

        with (
            patch("jobs.management.commands.scrape_jobs.scrape_company", return_value=456) as scrape_company,
            patch("jobs.management.commands.scrape_jobs.scrape_all") as scrape_all,
        ):
            call_command("scrape_jobs", "--company", "42", "--source", "greenhouse", stdout=stdout)

        scrape_company.assert_called_once_with(42, source="greenhouse")
        scrape_all.assert_not_called()
        output = stdout.getvalue()
        self.assertIn("Initializing scraping engine sequence for: greenhouse", output)
        self.assertIn("Scrape run 456 finished for company 42.", output)

    def test_rejects_non_integer_company_before_scraping_starts(self):
        stdout = StringIO()

        with (
            patch("jobs.management.commands.scrape_jobs.scrape_company") as scrape_company,
            patch("jobs.management.commands.scrape_jobs.scrape_all") as scrape_all,
        ):
            with self.assertRaises(CommandError) as error:
                call_command("scrape_jobs", "--company", "not-an-int", stdout=stdout)

        self.assertIn("invalid int value", str(error.exception))
        scrape_company.assert_not_called()
        scrape_all.assert_not_called()
        self.assertEqual(stdout.getvalue(), "")

    def test_propagates_scraper_failures_without_printing_success(self):
        stdout = StringIO()

        with patch(
            "jobs.management.commands.scrape_jobs.scrape_all",
            side_effect=RuntimeError("scraper backend unavailable"),
        ) as scrape_all:
            with self.assertRaisesMessage(RuntimeError, "scraper backend unavailable"):
                call_command("scrape_jobs", stdout=stdout)

        scrape_all.assert_called_once_with(source="https://mock-jobs-board.com")
        output = stdout.getvalue()
        self.assertIn("Initializing scraping engine sequence for: https://mock-jobs-board.com", output)
        self.assertNotIn("finished", output)
