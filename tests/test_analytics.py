import pytest
from drf_simple_apikey.analytics.models import ApiKeyAnalytics

from .fixtures.api_key import active_only_api_key
from .fixtures.user import user


@pytest.fixture
def api_key_analytics(user, active_only_api_key, db):
    return ApiKeyAnalytics.objects.create(api_key=active_only_api_key, request_number=0)


@pytest.mark.django_db
def test_add_endpoint_access(api_key_analytics, user, active_only_api_key):
    endpoint = "/api/data"
    ApiKeyAnalytics.objects.add_endpoint_access(
        api_key_id=active_only_api_key.id, endpoint=endpoint
    )

    # Fetch the updated object
    analytics = ApiKeyAnalytics.objects.get(api_key=active_only_api_key)
    assert endpoint in analytics.accessed_endpoints["endpoints"]
    assert analytics.accessed_endpoints["endpoints"][endpoint] == 1

    # Test incrementing the count
    ApiKeyAnalytics.objects.add_endpoint_access(
        api_key_id=active_only_api_key.id, endpoint=endpoint
    )
    analytics = ApiKeyAnalytics.objects.get(api_key=active_only_api_key)
    assert analytics.accessed_endpoints["endpoints"][endpoint] == 2


@pytest.mark.django_db
def test_get_most_accessed_endpoints(api_key_analytics, user, active_only_api_key):
    endpoints = ["/api/data", "/api/info", "/api/data"]
    for endpoint in endpoints:
        ApiKeyAnalytics.objects.add_endpoint_access(
            api_key_id=active_only_api_key.id, endpoint=endpoint
        )

    most_accessed = ApiKeyAnalytics.objects.get_most_accessed_endpoints(
        api_key_id=active_only_api_key.id
    )
    assert most_accessed[0][0] == "/api/data"  # Most accessed endpoint
    assert most_accessed[0][1] == 2  # Accessed twice


@pytest.mark.django_db
def test_str(api_key_analytics, user, active_only_api_key):
    assert (
        str(api_key_analytics) == f"API Key {api_key_analytics.api_key.name} Analytics"
    )
