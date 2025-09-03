from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('SEEKER', 'Job Seeker'),
        ('EMPLOYER', 'Employer'),
        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='SEEKER')


    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Job(models.Model):
    CATEGORY_CHOICES = (
        ('Software', 'Software'),
        ('Data', 'Data'),
        ('Design', 'Design'),
        ('Marketing', 'Marketing'),
        ('Finance', 'Finance'),
        ('Other', 'Other'),
        )


    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=120)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company_name}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('job', 'applicant') # one application per job per user
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"
