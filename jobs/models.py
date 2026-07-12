from django.db import models
from django.utils.text import slugify


class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    careers_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "companies"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class SkillTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Job(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    external_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    location = models.CharField(max_length=255, blank=True, default="Remote")
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    # Financial fields using Decimal for precise currency representation
    salary_min = models.DecimalField(max_length=12, decimal_places=2, max_digits=12, blank=True, null=True)
    salary_max = models.DecimalField(max_length=12, decimal_places=2, max_digits=12, blank=True, null=True)


    # Native Postgres JSONB field for raw unstructured scraper payloads
    raw_scraper_meta = models.JSONField(default=dict, blank=True)
    
    # Relationships
    tags = models.ManyToManyField(SkillTag, related_name='listings', blank=True)
    
    # Timestamps
    scraped_at = models.DateTimeField(auto_now=True)
    posted_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ["-posted_at", "-scraped_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "external_id"],
                condition=~models.Q(external_id=""),
                name="unique_company_external_id",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} @ {self.company.name}"


class ScrapeRun(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="scrape_runs",
        null=True,
        blank=True,
    )
    source = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    jobs_found = models.PositiveIntegerField(default=0)
    jobs_created = models.PositiveIntegerField(default=0)
    jobs_updated = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self) -> str:
        target = self.company.name if self.company else "all"
        return f"{self.source} scrape for {target} ({self.status})"
