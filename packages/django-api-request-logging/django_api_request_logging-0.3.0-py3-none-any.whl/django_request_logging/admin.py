from django.contrib import admin
from .models import RequestLog

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'method', 'status_code', 'timestamp')
    search_fields = ('endpoint', 'method')
    readonly_fields = ('endpoint', 'method', 'headers', 'payload', 'response', 'status_code', 'timestamp')
    list_filter = ('method', 'status_code', 'timestamp')