import pytest
from django.test import override_settings
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
def api_key_authentication():
    """Returns an instance of APIKeyAuthentication."""
    return APIKeyAuthentication()


class TestApiKeyAuthenticationWithIPManagement:
    """Tests for APIKeyAuthentication with IP address whitelisting and blacklisting."""

    def test_authenticate_valid_request_with_whitelisted_ip(
        self, valid_request_with_whitelisted_ip, api_key_authentication
    ):
        """Tests that a request from a whitelisted IP address is authenticated successfully."""
        entity, _ = api_key_authentication.authenticate(valid_request_with_whitelisted_ip)
        assert isinstance(entity, User)

    def test_authenticate_denied_for_blacklisted_ip(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that a request from a blacklisted IP address is denied."""
        factory = APIRequestFactory()
        api_key, key = active_api_key
        api_key.blacklisted_ips = ["127.0.0.1"]
        api_key.save()

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="127.0.0.1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        with pytest.raises(
            exceptions.AuthenticationFailed, match=r"Access denied from blacklisted IP."
        ):
            api_key_authentication.authenticate(request)

    def test_authenticate_denied_for_unlisted_ip_with_existing_whitelist(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that a request from an unlisted IP address is denied when a whitelist is active."""
        factory = APIRequestFactory()
        api_key, key = active_api_key
        api_key.whitelisted_ips = ["127.0.0.1"]
        api_key.save()

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="192.168.1.1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"Access restricted to specific IP addresses.",
        ):
            api_key_authentication.authenticate(request)

    def test_authenticate_allowed_for_unlisted_ip_with_empty_whitelist(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that a request from an unlisted IP address is allowed when the whitelist is empty."""
        factory = APIRequestFactory()
        _, key = active_api_key

        request = factory.get(
            "/test-request/",
            REMOTE_ADDR="10.0.0.1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        entity, _ = api_key_authentication.authenticate(request)
        assert isinstance(entity, User)

    def test_get_client_ip_ipv6(self, api_key_authentication):
        """Tests that IPv6 addresses are extracted and validated correctly."""
        factory = APIRequestFactory()

        # Direct REMOTE_ADDR IPv6
        req1 = factory.get("/", REMOTE_ADDR="2001:db8::1")
        assert api_key_authentication._get_client_ip(req1) == "2001:db8::1"

        # Compressed loopback IPv6
        req2 = factory.get("/", REMOTE_ADDR="::1")
        assert api_key_authentication._get_client_ip(req2) == "::1"

        # Proxy X-Forwarded-For with IPv6 using override_settings
        with override_settings(DRF_API_KEY={"IP_ADDRESS_HEADER": "HTTP_X_FORWARDED_FOR"}):
            req3 = factory.get(
                "/", HTTP_X_FORWARDED_FOR="2001:db8::1, 10.0.0.1", REMOTE_ADDR="127.0.0.1"
            )
            assert api_key_authentication._get_client_ip(req3) == "2001:db8::1"

    def test_get_client_ip_malformed_ips_and_headers(self, api_key_authentication):
        """Tests that malformed IPv4/IPv6 addresses and proxy headers return None."""
        factory = APIRequestFactory()

        # Malformed REMOTE_ADDR
        req1 = factory.get("/", REMOTE_ADDR="invalid_ip_string")
        assert api_key_authentication._get_client_ip(req1) is None

        req2 = factory.get("/", REMOTE_ADDR="2001:xyz::1")
        assert api_key_authentication._get_client_ip(req2) is None

        req3 = factory.get("/", REMOTE_ADDR="256.256.256.256")
        assert api_key_authentication._get_client_ip(req3) is None

        # Malformed X-Forwarded-For using override_settings
        with override_settings(DRF_API_KEY={"IP_ADDRESS_HEADER": "HTTP_X_FORWARDED_FOR"}):
            req4 = factory.get("/", HTTP_X_FORWARDED_FOR="not_an_ip, 10.0.0.1", REMOTE_ADDR="127.0.0.1")
            # Falls back to REMOTE_ADDR because first forwarded IP is invalid
            assert api_key_authentication._get_client_ip(req4) == "127.0.0.1"

            req5 = factory.get("/", HTTP_X_FORWARDED_FOR="invalid_ip", REMOTE_ADDR="invalid_remote")
            assert api_key_authentication._get_client_ip(req5) is None

    def test_authenticate_normalized_ipv6_matching(
        self, user, active_api_key, api_key_authentication
    ):
        """Tests that equivalent IPv6 representations (expanded vs compressed) match correctly."""
        factory = APIRequestFactory()
        api_key, key = active_api_key

        # Whitelist contains expanded IPv6, request sent with compressed form
        api_key.whitelisted_ips = ["2001:0db8:0000:0000:0000:0000:0000:0001"]
        api_key.save()

        request1 = factory.get(
            "/test-request/",
            REMOTE_ADDR="2001:db8::1",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )
        entity, _ = api_key_authentication.authenticate(request1)
        assert isinstance(entity, User)

        # Blacklist contains compressed IPv6, request sent with expanded form
        api_key.whitelisted_ips = []
        api_key.blacklisted_ips = ["2001:db8::1"]
        api_key.save()

        request2 = factory.get(
            "/test-request/",
            REMOTE_ADDR="2001:0db8:0000:0000:0000:0000:0000:0001",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )
        with pytest.raises(
            exceptions.AuthenticationFailed, match=r"Access denied from blacklisted IP."
        ):
            api_key_authentication.authenticate(request2)

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

