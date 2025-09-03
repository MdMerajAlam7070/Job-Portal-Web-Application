from django.apps import AppConfig
# from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        # import signals so they get registered when Django starts
        # use the full module path to avoid circular import surprises
        from . import signals  # noqa
# from django.apps import AppConfig

# class JobsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'jobs'

#     def ready(self):
#         try:
#             import jobs.signals  # noqa
#         except Exception:
#             pass
