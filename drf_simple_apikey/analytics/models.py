from __future__ import annotations

import re
import typing

from django.db import models
from drf_simple_apikey.settings import package_settings


def _sanitize_endpoint(endpoint: str) -> str:
    """
    Sanitize endpoint path to prevent injection and data pollution.
    - Remove dangerous characters
    - Limit length
    - Normalize path
    """
    if not endpoint:
        return ""

    # Limit length
    max_length = package_settings.MAX_ENDPOINT_LENGTH
    if len(endpoint) > max_length:
        endpoint = endpoint[:max_length]

    # Remove null bytes and other dangerous characters
    # Keep only printable ASCII characters and common URL characters
    endpoint = re.sub(r'[^\x20-\x7E/?#[\]@!$&\'()*+,;=]', '', endpoint)

    # Remove multiple consecutive slashes (except at start)
    endpoint = re.sub(r'/+', '/', endpoint)
    if endpoint.startswith('//'):
        endpoint = '/' + endpoint.lstrip('/')

    # Limit to reasonable path length
    if len(endpoint) > max_length:
        endpoint = endpoint[:max_length]

    return endpoint


class ApiKeyAnalyticsManager(models.Manager):
    def add_endpoint_access(self, api_key_id: int, endpoint: str) -> None:
        """
        Retrieve or create ApiKeyAnalytics instance and increment the endpoint access count.
        Sanitizes endpoint path before storage to prevent injection and data pollution.
        """
        # Sanitize endpoint path
        sanitized_endpoint = _sanitize_endpoint(endpoint)

        # Skip if endpoint is empty after sanitization
        if not sanitized_endpoint:
            return

        obj, created = self.get_or_create(
            api_key_id=api_key_id, defaults={"accessed_endpoints": {"endpoints": {}}}
        )

        # Initialize endpoints dictionary if it doesn't exist
        if "endpoints" not in obj.accessed_endpoints:
            obj.accessed_endpoints["endpoints"] = {}

        # Check endpoint limit
        max_endpoints = package_settings.MAX_ENDPOINTS_PER_KEY
        current_endpoints = obj.accessed_endpoints["endpoints"]

        # If we're at the limit and this is a new endpoint, skip it
        if len(current_endpoints) >= max_endpoints and sanitized_endpoint not in current_endpoints:
            return

        # Increment endpoint count
        current_endpoints[sanitized_endpoint] = (
            current_endpoints.get(sanitized_endpoint, 0) + 1
        )
        obj.request_number += 1
        obj.save()

    def get_most_accessed_endpoints(
        self, api_key_id: int
    ) -> list[tuple[str, int]]:
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

    def __str__(self) -> str:
        return f"API Key {self.api_key.name} Analytics"
