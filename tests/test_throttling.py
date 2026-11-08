"""
Tests for APIKeyRateThrottle.

Covers:
  - validate_throttle_rate validator (model-level)
  - get_cache_key: None for non-API-key requests, pk-scoped for API keys
  - get_rate: falls back gracefully when no DEFAULT_THROTTLE_RATES["api_key"]
  - allow_request: global rate, per-key rate override, no rate = unlimited,
    invalid throttle_rate on a key → warning logged + falls back to global,
    unauthenticated requests are ignored (not throttled)
"""
from __future__ import annotations

import pytest
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from drf_simple_apikey.models import APIKey, validate_throttle_rate
from drf_simple_apikey.throttling import APIKeyRateThrottle

from .fixtures.user import user  # noqa: F401 – pytest fixture
from .fixtures.api_key import active_api_key  # noqa: F401 – pytest fixture

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_authed_request(key_str: str) -> object:
    """Return a GET request carrying the given raw API key string."""
    from drf_simple_apikey.settings import package_settings

    return factory.get(
        "/",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key_str}",
    )


def _attach_api_key(request, api_key_obj):
    """Simulate DRF having already set request.auth to the APIKey instance."""
    request.auth = api_key_obj
    return request


def _anon_request():
    return factory.get("/")


# ---------------------------------------------------------------------------
# validate_throttle_rate
# ---------------------------------------------------------------------------


class TestValidateThrottleRate:
    """Unit tests for the model-level validator."""

    @pytest.mark.parametrize(
        "value",
        ["100/hour", "10/minute", "1/second", "5000/day", "1/h", "60/m", "1/s", "1/d"],
    )
    def test_valid_rates_do_not_raise(self, value):
        # Should complete without raising
        validate_throttle_rate(value)

    @pytest.mark.parametrize(
        "value",
        [
            "hundred/hour",  # non-numeric count
            "100/week",      # 'w' is not an accepted period initial
            "100",           # missing slash + period
            "/hour",         # missing count
            "100/",          # missing period
            "-1/hour",       # negative count
        ],
    )
    def test_invalid_rates_raise_validation_error(self, value):
        with pytest.raises(ValidationError):
            validate_throttle_rate(value)

    def test_empty_string_is_allowed(self):
        """Empty string means 'use global rate' — must not raise."""
        validate_throttle_rate("")

    def test_none_is_allowed(self):
        """None is treated as 'no value' — must not raise."""
        validate_throttle_rate(None)


# ---------------------------------------------------------------------------
# get_cache_key
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestGetCacheKey:
    def test_returns_none_for_unauthenticated_request(self):
        throttle = APIKeyRateThrottle()
        request = _anon_request()
        request.auth = None

        assert throttle.get_cache_key(request, view=None) is None

    def test_returns_none_when_auth_is_not_an_api_key(self):
        throttle = APIKeyRateThrottle()
        request = _anon_request()
        request.auth = object()  # something that is not an AbstractAPIKey

        assert throttle.get_cache_key(request, view=None) is None

    def test_returns_pk_scoped_key_for_api_key_request(self, active_api_key):
        api_key, _ = active_api_key
        throttle = APIKeyRateThrottle()
        request = _anon_request()
        _attach_api_key(request, api_key)

        cache_key = throttle.get_cache_key(request, view=None)

        assert cache_key is not None
        assert str(api_key.pk) in cache_key
        assert "api_key" in cache_key

    def test_two_distinct_keys_produce_different_cache_keys(self, user):  # noqa: F811
        api_key1, _ = APIKey.objects.create_api_key(entity=user)
        api_key2, _ = APIKey.objects.create_api_key(entity=user)

        throttle = APIKeyRateThrottle()

        req1 = _anon_request()
        _attach_api_key(req1, api_key1)
        req2 = _anon_request()
        _attach_api_key(req2, api_key2)

        assert throttle.get_cache_key(req1, None) != throttle.get_cache_key(req2, None)


# ---------------------------------------------------------------------------
# get_rate
# ---------------------------------------------------------------------------


class TestGetRate:
    def test_returns_none_when_no_global_rate_configured(self, settings):
        """No DEFAULT_THROTTLE_RATES → no ImproperlyConfigured crash, just None."""
        settings.REST_FRAMEWORK = {}
        throttle = APIKeyRateThrottle()
        assert throttle.get_rate() is None

    def test_returns_configured_global_rate(self, settings):
        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "200/hour"}}
        throttle = APIKeyRateThrottle()
        assert throttle.get_rate() == "200/hour"


# ---------------------------------------------------------------------------
# allow_request
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestAllowRequest:
    def setup_method(self):
        cache.clear()

    def test_unauthenticated_request_is_not_throttled(self, settings):
        """Requests without an API key must always be allowed (get_cache_key → None)."""
        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "1/day"}}
        throttle = APIKeyRateThrottle()
        request = _anon_request()
        request.auth = None

        # Even if we call it many times it should never be throttled
        for _ in range(10):
            assert throttle.allow_request(request, view=None) is True

    def test_request_allowed_within_global_rate(self, settings, active_api_key):
        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "5/minute"}}
        api_key, _ = active_api_key

        for _ in range(5):
            throttle = APIKeyRateThrottle()
            request = _anon_request()
            _attach_api_key(request, api_key)
            assert throttle.allow_request(request, view=None) is True

    def test_request_blocked_once_global_rate_exceeded(self, settings, active_api_key):
        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "2/minute"}}
        api_key, _ = active_api_key

        def _do_request():
            t = APIKeyRateThrottle()
            req = _anon_request()
            _attach_api_key(req, api_key)
            return t.allow_request(req, view=None)

        assert _do_request() is True
        assert _do_request() is True
        assert _do_request() is False  # 3rd request must be blocked

    def test_per_key_rate_overrides_global_rate(self, settings, user):  # noqa: F811
        """A key with throttle_rate="1/minute" is blocked on the 2nd request
        even if the global rate would allow more."""
        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "100/minute"}}

        api_key, _ = APIKey.objects.create_api_key(entity=user, throttle_rate="1/minute")

        def _do_request():
            t = APIKeyRateThrottle()
            req = _anon_request()
            _attach_api_key(req, api_key)
            return t.allow_request(req, view=None)

        assert _do_request() is True
        assert _do_request() is False  # blocked by per-key rate

    def test_no_rate_anywhere_means_unlimited(self, settings, active_api_key):
        """With no global rate and no per-key rate, requests are never throttled."""
        settings.REST_FRAMEWORK = {}
        api_key, _ = active_api_key

        for _ in range(20):
            t = APIKeyRateThrottle()
            req = _anon_request()
            _attach_api_key(req, api_key)
            assert t.allow_request(req, view=None) is True

    def test_invalid_per_key_rate_logs_warning_and_falls_back_to_global(
        self, settings, user, caplog  # noqa: F811
    ):
        """An unparseable throttle_rate on the key must log a warning and
        fall back to the global rate instead of raising."""
        import logging

        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "100/minute"}}

        # Bypass the validator to store a deliberately bad rate
        api_key, _ = APIKey.objects.create_api_key(entity=user)
        APIKey.objects.filter(pk=api_key.pk).update(throttle_rate="not-a-valid-rate")
        api_key.refresh_from_db()

        with caplog.at_level(logging.WARNING, logger="drf_simple_apikey.throttling"):
            t = APIKeyRateThrottle()
            req = _anon_request()
            _attach_api_key(req, api_key)
            result = t.allow_request(req, view=None)

        assert result is True  # falls back to global → allowed
        assert any(
            "Ignoring invalid throttle rate" in r.message for r in caplog.records
        )

    def test_two_keys_have_independent_budgets(self, settings, user):  # noqa: F811
        """Exhausting one key's budget must not affect another key's budget."""
        settings.REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"api_key": "1/minute"}}
        api_key1, _ = APIKey.objects.create_api_key(entity=user)
        api_key2, _ = APIKey.objects.create_api_key(entity=user)

        def _do(api_key):
            t = APIKeyRateThrottle()
            req = _anon_request()
            _attach_api_key(req, api_key)
            return t.allow_request(req, view=None)

        # Exhaust key1
        assert _do(api_key1) is True
        assert _do(api_key1) is False

        # key2 should still be fine
        assert _do(api_key2) is True

