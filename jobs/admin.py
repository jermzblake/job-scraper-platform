from django.contrib import admin

from .models import Company, Job, ScrapeRun


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "careers_url", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "status", "posted_at", "scraped_at")
    list_filter = ("status", "company")
    search_fields = ("title", "external_id", "location")
    raw_id_fields = ("company",)


@admin.register(ScrapeRun)
class ScrapeRunAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "company",
        "status",
        "jobs_found",
        "jobs_created",
        "started_at",
        "finished_at",
    )
    list_filter = ("status", "source")
    raw_id_fields = ("company",)
    readonly_fields = ("started_at",)
