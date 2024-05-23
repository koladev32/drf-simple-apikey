from drf_simple_apikey.analytics.models import ApiKeyAnalytics
from drf_simple_apikey.crypto import get_crypto
from drf_simple_apikey.parser import APIKeyParser
from drf_simple_apikey.utils import get_key


class ApiKeyAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        key = get_key(APIKeyParser(), request)

        payload = get_crypto().decrypt(key)

        # Use the custom manager to handle endpoint access logging
        ApiKeyAnalytics.objects.add_endpoint_access(
            api_key_id=payload["_pk"], endpoint=request.path
        )

        return response
