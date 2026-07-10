from dataclasses import dataclass
from datetime import datetime


@dataclass
class ParsedJob:
    external_id: str
    title: str
    url: str
    location: str = ""
    description: str = ""
    posted_at: datetime | None = None


def parse_jobs(source: str, raw_content: str) -> list[ParsedJob]:
    """Parse raw content into normalized job records for a given source."""
    raise NotImplementedError(f"No parser registered for source: {source}")
