import pytest
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.test import APIRequestFactory

from drf_simple_apikey.backends import APIKeyAuthentication
from drf_simple_apikey.settings import package_settings
from .fixtures.api_key import active_api_key
from .fixtures.user import user

pytestmark = pytest.mark.django_db


@pytest.fixture
def valid_request_with_whitelisted_ip(user, active_api_key):
    """Creates a valid request from a whitelisted IP address."""
    factory = APIRequestFactory()
    api_key, key = active_api_key
    api_key.whitelisted_ips = ["127.0.0.1"]
    api_key.save()

    return factory.get(
        "/test-request/",
        REMOTE_ADDR="127.0.0.1",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.fixture
def valid_request_with_blacklisted_ip(user, active_api_key):
    """Creates a request from a blacklisted IP address."""
    factory = APIRequestFactory()
    api_key, key = active_api_key
    api_key.blacklisted_ips = ["127.0.0.1"]
    api_key.save()

    return factory.get(
        "/test-request/",
        REMOTE_ADDR="127.0.0.1",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.fixture
def request_with_unlisted_ip(user, active_api_key):
    """Creates a request from an IP that is neither whitelisted nor blacklisted."""
    factory = APIRequestFactory()
    api_key, key = active_api_key
    api_key.whitelisted_ips = ["192.168.0.1"]  # Different IP than the request IP
    api_key.save()

    return factory.get(
        "/test-request/",
        REMOTE_ADDR="10.0.0.1",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.fixture
def api_key_authentication():
    return APIKeyAuthentication()


@pytest.mark.django_db
class TestApiKeyAuthenticationWithIPManagement:
    pytestmark = pytest.mark.django_db

    def test_authenticate_valid_request_with_whitelisted_ip(
        self, valid_request_with_whitelisted_ip, api_key_authentication
    ):
        """Tests that a request from a whitelisted IP is authenticated successfully."""
        entity, _ = api_key_authentication.authenticate(
            valid_request_with_whitelisted_ip
        )
        assert isinstance(entity, User)

    def test_authenticate_denied_for_blacklisted_ip(
        self, valid_request_with_blacklisted_ip, api_key_authentication
    ):
        """Tests that a request from a blacklisted IP is denied."""
        with pytest.raises(
            exceptions.AuthenticationFailed, match=r"Access denied from blacklisted IP."
        ):
            api_key_authentication.authenticate(valid_request_with_blacklisted_ip)

    def test_authenticate_denied_for_unlisted_ip_with_existing_whitelist(
        self, request_with_unlisted_ip, api_key_authentication
    ):
        """Tests that a request from an IP not in the whitelist is denied if a whitelist exists."""
        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"Access restricted to specific IP addresses.",
        ):
            api_key_authentication.authenticate(request_with_unlisted_ip)

    def test_authenticate_allowed_for_request_with_no_ip_restrictions(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that a request with no IP restrictions is authenticated successfully."""
        factory = APIRequestFactory()
        _, key = active_api_key

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="10.0.0.1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        entity, _ = api_key_authentication.authenticate(request)
        assert isinstance(entity, User)
