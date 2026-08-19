import pytest
from rest_framework import exceptions
from rest_framework.test import APIRequestFactory

from drf_simple_apikey.backends import APIKeyAuthentication
from drf_simple_apikey.settings import package_settings

from .fixtures.api_key import active_api_key
from .fixtures.user import user

pytestmark = pytest.mark.django_db


def set_enforce_https(settings, value):
    # Merge into the existing DRF_API_KEY rather than replacing it wholesale,
    # so FERNET_SECRET stays whatever conftest.py configured - active_api_key
    # encrypts its key with that secret, and swapping in a different one here
    # would break decryption of a key the fixture already created.
    settings.DRF_API_KEY = {**settings.DRF_API_KEY, "ENFORCE_HTTPS": value}


def request_for(key, *, secure=False):
    factory = APIRequestFactory()
    return factory.get(
        "/test-request/",
        secure=secure,
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


class TestHttpsEnforcement:
    def test_disabled_by_default_in_this_test_environment(self):
        # conftest.py sets ENFORCE_HTTPS=False explicitly for the test
        # suite (DEBUG isn't set, so it defaults to False, which would
        # otherwise auto-enforce HTTPS).
        assert package_settings.ENFORCE_HTTPS is False

    def test_enforced_denies_insecure_request(self, settings, user, active_api_key):
        set_enforce_https(settings, True)
        _, key = active_api_key

        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"API key authentication requires HTTPS\.",
        ):
            APIKeyAuthentication().authenticate(request_for(key, secure=False))

    def test_enforced_allows_secure_request(self, settings, user, active_api_key):
        set_enforce_https(settings, True)
        _, key = active_api_key

        entity, _ = APIKeyAuthentication().authenticate(request_for(key, secure=True))

        assert entity == user

    def test_enforced_allows_forwarded_https(self, settings, user, active_api_key):
        set_enforce_https(settings, True)
        _, key = active_api_key
        factory = APIRequestFactory()
        request = factory.get(
            "/test-request/",
            HTTP_X_FORWARDED_PROTO="https",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
        )

        entity, _ = APIKeyAuthentication().authenticate(request)

        assert entity == user

    def test_disabled_allows_insecure_request(self, settings, user, active_api_key):
        set_enforce_https(settings, False)
        _, key = active_api_key

        entity, _ = APIKeyAuthentication().authenticate(request_for(key, secure=False))

        assert entity == user

    def test_auto_detect_follows_debug_when_unset(self, settings, user, active_api_key):
        # ENFORCE_HTTPS omitted entirely -> auto-detect from DEBUG, with no
        # test-framework sniffing: DEBUG=True means HTTPS is not enforced.
        settings.DEBUG = True
        drf_api_key = {**settings.DRF_API_KEY}
        drf_api_key.pop("ENFORCE_HTTPS", None)
        settings.DRF_API_KEY = drf_api_key
        _, key = active_api_key

        entity, _ = APIKeyAuthentication().authenticate(request_for(key, secure=False))

        assert entity == user
