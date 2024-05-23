from django.db import models
from rest_framework_simple_api_key.settings import package_settings


class ApiKeyAnalyticsManager(models.Manager):
    def add_endpoint_access(self, api_key_id, endpoint):
        """
        Retrieve or create ApiKeyAnalytics instance and increment the endpoint access count.
        """
        obj, created = self.get_or_create(
            api_key_id=api_key_id, defaults={"accessed_endpoints": {"endpoints": {}}}
        )

        # Initialize endpoints dictionary if it doesn't exist
        if "endpoints" not in obj.accessed_endpoints:
            obj.accessed_endpoints["endpoints"] = {}

        # Increment endpoint count
        obj.accessed_endpoints["endpoints"][endpoint] = (
            obj.accessed_endpoints["endpoints"].get(endpoint, 0) + 1
        )
        obj.request_number += 1
        obj.save()

    def get_most_accessed_endpoints(self, api_key_id):
        """
        Returns the most accessed endpoints for a given API key, sorted by access count.
        """
        obj = self.get(api_key_id=api_key_id)
        if (
            "endpoints" in obj.accessed_endpoints
            and obj.accessed_endpoints["endpoints"]
        ):
            return sorted(
                obj.accessed_endpoints["endpoints"].items(),
                key=lambda item: item[1],
                reverse=True,
            )
        return []


class ApiKeyAnalytics(models.Model):
    api_key = models.ForeignKey(
        package_settings.API_KEY_CLASS,
        on_delete=models.CASCADE,
        related_name="analytics",
    )
    request_number = models.IntegerField(default=0)
    accessed_endpoints = models.JSONField(default=dict)

    objects = ApiKeyAnalyticsManager()

    def __str__(self):
        return f"API Key {self.api_key.name} Analytics"
