from django.apps import AppConfig

class RequestLoggingModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_request_logging'
    verbose_name = 'Request Logging Module'