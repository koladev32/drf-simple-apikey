from unittest import mock

import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from drf_simple_apikey.analytics.middleware import ApiKeyAnalyticsMiddleware
from drf_simple_apikey.analytics.models import ApiKeyAnalytics
from .fixtures.api_key import active_api_key
from .fixtures.user import user
from drf_simple_apikey.settings import package_settings


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
    """Return a request factory."""
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


@pytest.mark.django_db
def test_middleware_ignores_admin_routes(middleware, request_factory):
    """Test that middleware ignores admin routes."""
    # Create a request to admin path
    request = request_factory.get("/admin/")
    
    # Call middleware
    response = middleware(request)
    
    # Check the response
    assert response.status_code == 200
    
    # Verify no analytics were created
    assert not ApiKeyAnalytics.objects.exists()


@pytest.mark.django_db
def test_middleware_ignores_custom_routes(middleware, request_factory, settings):
    """Test that middleware ignores custom routes specified in settings."""
    # Add custom route to ignore
    settings.DRF_API_KEY = {
        "IGNORED_ROUTES": ["/admin/", "/api/documents/"]
    }
    
    # Create a request to custom ignored path
    request = request_factory.get("/api/documents/123")
    
    # Call middleware
    response = middleware(request)
    
    # Check the response
    assert response.status_code == 200
    
    # Verify no analytics were created
    assert not ApiKeyAnalytics.objects.exists()


@pytest.mark.django_db
def test_middleware_processes_admin_when_not_ignored(middleware, request_factory, settings):
    """Test that middleware processes admin routes when they are not in IGNORED_ROUTES."""
    # Remove admin from ignored routes
    settings.DRF_API_KEY = {
        "IGNORED_ROUTES": []  # Empty list means no routes are ignored
    }
    
    # Create a request to admin path
    request = request_factory.get("/admin/")
    
    # Call middleware
    response = middleware(request)
    
    # Check that the response is processed normally
    assert response.status_code == 200


@pytest.mark.django_db
def test_middleware_processes_non_ignored_routes(middleware, user, active_api_key, request_factory):
    """Test that middleware processes routes that are not in the ignored list."""
    apikey, key = active_api_key
    
    # Create a request to a non-ignored path
    request = request_factory.get("/api/other/123")
    
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
        
        # Verify analytics were created
        analytics = ApiKeyAnalytics.objects.get(api_key_id=apikey.pk)
        assert "/api/other/123" in analytics.accessed_endpoints["endpoints"]


@pytest.mark.django_db
def test_middleware_handles_invalid_api_key(middleware, request_factory):
    """Test that middleware handles invalid API keys gracefully."""
    # Create a request with no API key
    request = request_factory.get("/api/some-path")
    
    # Call middleware
    response = middleware(request)
    
    # Check the response
    assert response.status_code == 200
    
    # Verify no analytics were created
    assert not ApiKeyAnalytics.objects.exists()
