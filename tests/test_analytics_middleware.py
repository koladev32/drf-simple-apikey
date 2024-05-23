from unittest import mock

import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from drf_simple_apikey.analytics.middleware import ApiKeyAnalyticsMiddleware
from drf_simple_apikey.analytics.models import ApiKeyAnalytics
from .fixtures.api_key import active_api_key
from .fixtures.user import user


@pytest.fixture
def api_key_analytics(user, active_api_key, db):
    apikey, _ = active_api_key
    return ApiKeyAnalytics.objects.create(api_key=apikey, request_number=0)


@pytest.fixture
def middleware():
    """Return an instance of the middleware."""
    return ApiKeyAnalyticsMiddleware(get_response=lambda request: HttpResponse())


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.mark.django_db
def test_api_key_analytics_middleware(
    middleware, user, active_api_key, request_factory
):
    apikey, key = active_api_key
    # Create a mock request
    request = request_factory.get("/some-path")

    # Assume get_key and get_crypto are properly mocked to return expected values
    with mock.patch(
        "drf_simple_apikey.parser.APIKeyParser.get", return_value=key
    ), mock.patch(
        "drf_simple_apikey.crypto.ApiCrypto.decrypt",
        return_value={"_pk": apikey.pk},
    ):
        # Call middleware
        response = middleware(request)

        # Check the response
        assert response.status_code == 200

        # Check if ApiKeyAnalytics was updated
        analytics = ApiKeyAnalytics.objects.get(api_key_id=apikey.pk)
        assert "/some-path" in analytics.accessed_endpoints["endpoints"]
