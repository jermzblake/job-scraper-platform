from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Job


def job_list(request: HttpRequest) -> HttpResponse:
    jobs = Job.objects.select_related("company").filter(status=Job.Status.ACTIVE)
    return render(request, "jobs/job_list.html", {"jobs": jobs})


def job_detail(request: HttpRequest, pk: int) -> HttpResponse:
    job = get_object_or_404(Job.objects.select_related("company"), pk=pk)
    return render(request, "jobs/job_detail.html", {"job": job})
