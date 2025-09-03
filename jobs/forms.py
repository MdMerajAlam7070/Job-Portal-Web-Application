# jobs/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Application, Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title", "description", "company_name",
            "location", "category", "salary_min", "salary_max"
        ]

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "cover_letter"]
