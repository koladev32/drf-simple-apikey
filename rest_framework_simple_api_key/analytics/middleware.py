from rest_framework_simple_api_key.analytics.models import ApiKeyAnalytics
from rest_framework_simple_api_key.backends import get_key
from rest_framework_simple_api_key.crypto import get_crypto
from rest_framework_simple_api_key.parser import APIKeyParser


class ApiKeyAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        key = get_key(APIKeyParser(), request)

        api_key = get_crypto().decrypt(key)

        try:
            analytic = ApiKeyAnalytics.objects.get(api_key=api_key)
            analytic.request_number += 1
            analytic.accessed_endpoints['endpoints'].append(request.url)
            analytic.save()
        except ApiKeyAnalytics.DoesNotExist:

            ApiKeyAnalytics.objects.create(
                api_key_id=api_key,
                request_number=1,
                accessed_endpoints={"endpoints": [request.url]},
            )

        return response
