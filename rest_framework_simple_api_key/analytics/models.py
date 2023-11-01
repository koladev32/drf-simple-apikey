from django.db import models

from rest_framework_simple_api_key.settings import package_settings


class ApiKeyAnalytics(models.Model):
    api_key = models.ForeignKey(
        package_settings.API_KEY_CLASS,
        on_delete=models.CASCADE,
        related_name="analytics",
    )
    request_number = models.IntegerField(default=0)
    accessed_endpoints = models.JSONField()

    @property
    def most_accessed_endpoints(self):
        # TODO  : Make the treatment with accessed_endpoints
        return []
