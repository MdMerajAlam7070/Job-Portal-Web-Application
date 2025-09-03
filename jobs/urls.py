# jobs/urls.py
from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/post/", views.post_job, name="post_job"),
    path("jobs/manage/", views.manage_jobs, name="manage_jobs"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("jobs/<int:pk>/edit/", views.edit_job, name="edit_job"),
    path("jobs/<int:pk>/delete/", views.delete_job, name="delete_job"),
    path("jobs/<int:pk>/applications/", views.applications_view, name="applications"),
]
