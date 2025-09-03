# jobs/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm, JobForm, ApplicationForm
from .models import Job, Application, Profile


from django.db.models import Q
from django.http import JsonResponse


@require_http_methods(["GET"])
def ajax_search_jobs(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    qs = Job.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(company_name__icontains=query) |
        Q(location__icontains=query) |
        Q(category__icontains=query)
    )[:10]

    results = [
        {"id": job.id, "title": job.title, "company": job.company_name, "location": job.location}
        for job in qs
    ]
    return JsonResponse(results, safe=False)


# Landing / index
@require_http_methods(["GET"])
def index(request):
    recent = Job.objects.all()[:6]
    return render(request, "jobs/index.html", {"latest_jobs": recent})

# Register
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set profile role (Profile created by signal)
            role = form.cleaned_data.get("role")
            user.profile.role = role
            user.profile.save()
            messages.success(request, "Account created. Please login.")
            return redirect("jobs:login")
    else:
        form = RegistrationForm()
    return render(request, "jobs/register.html", {"form": form})

# Login
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("jobs:index")
        messages.error(request, "Invalid credentials")
    return render(request, "jobs/login.html")

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect("jobs:index")

# Job list + filters
@require_http_methods(["GET"])
def job_list(request):
    qs = Job.objects.all()
    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    category = request.GET.get("category", "").strip()
    company = request.GET.get("company", "").strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if location:
        qs = qs.filter(location__icontains=location)
    if category:
        qs = qs.filter(category__iexact=category)
    if company:
        qs = qs.filter(company_name__icontains=company)

    return render(request, "jobs/job_list.html", {
        "jobs": qs,
        "q": q,
        "location": location,
        "category": category,
        "company": company,
    })

# Job detail + apply
@require_http_methods(["GET", "POST"])
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Please login to apply.")
            return redirect("jobs:login")
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Prevent double application
            app, created = Application.objects.get_or_create(
                job=job,
                applicant=request.user,
                defaults={
                    "resume": form.cleaned_data["resume"],
                    "cover_letter": form.cleaned_data.get("cover_letter", ""),
                },
            )
            if not created:
                messages.info(request, "You already applied to this job.")
            else:
                messages.success(request, "Application submitted!")
            return redirect("jobs:job_detail", pk=pk)
    else:
        form = ApplicationForm()
    return render(request, "jobs/job_detail.html", {"job": job, "form": form})

# Post job (Employer only)
@login_required
@require_http_methods(["GET", "POST"])
def post_job(request):
    if request.user.profile.role != "EMPLOYER":
        messages.error(request, "Only employers can post jobs.")
        return redirect("jobs:job_list")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect("jobs:manage_jobs")
    else:
        form = JobForm()
    return render(request, "jobs/post_job.html", {"form": form})

# Manage jobs (Employer)
@login_required
@require_http_methods(["GET"])
def manage_jobs(request):
    if request.user.profile.role != "EMPLOYER":
        messages.error(request, "Only employers can access.")
        return redirect("jobs:job_list")
    my_jobs = Job.objects.filter(posted_by=request.user)
    return render(request, "jobs/manage_jobs.html", {"jobs": my_jobs})

# Edit job
@login_required
@require_http_methods(["GET", "POST"])
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect("jobs:manage_jobs")
    else:
        form = JobForm(instance=job)
    return render(request, "jobs/post_job.html", {"form": form, "edit_mode": True})

# Delete job
@login_required
@require_http_methods(["POST"])
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    job.delete()
    messages.success(request, "Job deleted.")
    return redirect("jobs:manage_jobs")

# View applications for a job (Employer)
@login_required
@require_http_methods(["GET"])
def applications_view(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    apps = job.applications.select_related("applicant").all()
    return render(request, "jobs/applications.html", {"job": job, "applications": apps})
