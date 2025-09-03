from django.contrib import admin
from .models import Job, Application, Profile  # import models from this app

# Register your models
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Profile)

