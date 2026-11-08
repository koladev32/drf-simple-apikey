from __future__ import annotations

import logging
import typing

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from rest_framework.throttling import SimpleRateThrottle

from drf_simple_apikey.models import AbstractAPIKey

logger = logging.getLogger(__name__)


class APIKeyRateThrottle(SimpleRateThrottle):
    """
    Limits how many requests each API key can make, using DRF's sliding
    window throttle.

    The limit is counted per API key, not per user or IP: two keys of same
    user each get their own budget.

    The rate comes from, in order:

    1. the key's own: `throttle_rate` field, eg. "100/hour";
    2. `REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["api_key"]`.

    With neither set, the key is not throttled. Requests that were not
    authenticated with an API key are ignored; combine the class with
    `AnonRateThrottle` to limit those.
    """

    scope = "api_key"

    @property
    def THROTTLE_RATES(self) -> dict[str, str | None]:
        from rest_framework.settings import api_settings

        return api_settings.DEFAULT_THROTTLE_RATES

    def get_rate(self) -> str | None:
        try:
            return super().get_rate()
        except ImproperlyConfigured:
            return None

    @staticmethod
    def _get_api_key(request: HttpRequest) -> AbstractAPIKey | None:
        api_key = getattr(request, "auth", None)
        return api_key if isinstance(api_key, AbstractAPIKey) else None

    def _use_key_rate(self, api_key: AbstractAPIKey) -> None:
        try:
            num_requests, duration = self.parse_rate(api_key.throttle_rate)
        except (ValueError, KeyError, IndexError):
            logger.warning(
                "Ignoring invalid throttle rate on API Key",
                extra={
                    "api_key_id": api_key.pk,
                    "throttle_rate": api_key.throttle_rate,
                },
            )
            return
        self.rate = api_key.throttle_rate
        self.num_requests, self.duration = num_requests, duration

    def allow_request(self, request: HttpRequest, view: typing.Any) -> bool:
        api_key = self._get_api_key(request)
        if api_key is not None and api_key.throttle_rate:
            self._use_key_rate(api_key)

        return super().allow_request(request, view)

    def get_cache_key(self, request: HttpRequest, view: typing.Any) -> str | None:
        api_key = self._get_api_key(request)
        if api_key is None:
            return None

        return self.cache_format % {"scope": self.scope, "ident": api_key.pk}
