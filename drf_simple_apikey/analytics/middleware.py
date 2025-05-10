from drf_simple_apikey.analytics.models import ApiKeyAnalytics
from drf_simple_apikey.crypto import get_crypto
from drf_simple_apikey.parser import APIKeyParser
from drf_simple_apikey.utils import get_key
from drf_simple_apikey.settings import package_settings


class ApiKeyAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the current path should be ignored
        if any(request.path.startswith(route) for route in package_settings.IGNORED_ROUTES):
            return self.get_response(request)

        response = self.get_response(request)

        try:
            key = get_key(APIKeyParser(), request)
            payload = get_crypto().decrypt(key)

            # Use the custom manager to handle endpoint access logging
            ApiKeyAnalytics.objects.add_endpoint_access(
                api_key_id=payload["_pk"], endpoint=request.path
            )
        except Exception:
            # If there's any error with API key processing, just continue
            pass

        return response
