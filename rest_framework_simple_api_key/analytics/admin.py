from django.contrib import admin
from .models import ApiKeyAnalytics


class ApiKeyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("id", "request_number", "accessed_endpoints", "api_key")

    list_filter = (
        "request_number",
        "api_key",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ApiKeyAnalytics, ApiKeyAnalyticsAdmin)
