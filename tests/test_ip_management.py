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

    def test_get_client_ip_ipv6(self, api_key_authentication, settings):
        """Tests that IPv6 addresses are extracted and validated correctly."""
        factory = APIRequestFactory()

        # Direct REMOTE_ADDR IPv6
        req1 = factory.get("/", REMOTE_ADDR="2001:db8::1")
        assert api_key_authentication._get_client_ip(req1) == "2001:db8::1"

        # Compressed loopback IPv6
        req2 = factory.get("/", REMOTE_ADDR="::1")
        assert api_key_authentication._get_client_ip(req2) == "::1"

        # Proxy X-Forwarded-For with IPv6
        old_header = package_settings.IP_ADDRESS_HEADER
        package_settings.IP_ADDRESS_HEADER = "HTTP_X_FORWARDED_FOR"
        try:
            req3 = factory.get("/", HTTP_X_FORWARDED_FOR="2001:db8::1, 10.0.0.1", REMOTE_ADDR="127.0.0.1")
            assert api_key_authentication._get_client_ip(req3) == "2001:db8::1"
        finally:
            package_settings.IP_ADDRESS_HEADER = old_header

    def test_authenticate_valid_request_with_whitelisted_ipv6(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that a request from a whitelisted IPv6 address is authenticated successfully."""
        factory = APIRequestFactory()
        api_key, key = active_api_key
        api_key.whitelisted_ips = ["2001:db8::1"]
        api_key.save()

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="2001:db8::1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        entity, _ = api_key_authentication.authenticate(request)
        assert isinstance(entity, User)

    def test_authenticate_denied_for_blacklisted_ipv6(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that a request from a blacklisted IPv6 address is denied."""
        factory = APIRequestFactory()
        api_key, key = active_api_key
        api_key.blacklisted_ips = ["2001:db8::1"]
        api_key.save()

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="2001:db8::1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        with pytest.raises(
            exceptions.AuthenticationFailed, match=r"Access denied from blacklisted IP."
        ):
            api_key_authentication.authenticate(request)

    def test_authenticate_denied_for_unlisted_ipv6_with_existing_whitelist(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that an unlisted IPv6 request is denied when a whitelist is active."""
        factory = APIRequestFactory()
        api_key, key = active_api_key
        api_key.whitelisted_ips = ["2001:db8::1"]
        api_key.save()

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="2001:db8::999",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"Access restricted to specific IP addresses.",
        ):
            api_key_authentication.authenticate(request)

