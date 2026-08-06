from __future__ import annotations

import typing

from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed

from drf_simple_apikey.settings import package_settings


class APIKeyParser:
    """
    This is a custom parser used to retrieve the API Key from the
    authorization header. You can add custom parsing validation here.
    """

    keyword = package_settings.AUTHENTICATION_KEYWORD_HEADER

    def get(self, request: HttpRequest) -> str | None:
        return self.get_from_authorization(request)

    def get_from_authorization(self, request: HttpRequest) -> str | None:
        authorization = request.META.get("HTTP_AUTHORIZATION")

        if not authorization:
            # No Authorization header at all: this isn't an attempt to use
            # this scheme, so let DRF try the next authentication class
            # instead of failing the request outright.
            return None

        parts = authorization.split()

        if not parts or parts[0] != self.keyword:
            # Present, but not our keyword (e.g. "Bearer ..."): again, not
            # an attempt to use this scheme.
            return None

        if len(parts) != 2:
            # Our keyword is present, so this *is* an attempt to use this
            # scheme, just a malformed one (missing key, or extra spaces
            # inside it) — that's worth a real error instead of a silent
            # fall-through.
            raise AuthenticationFailed("Incorrect API KEY format.")

        return parts[1]

    def get_from_header(self, request: HttpRequest, name: str) -> str | None:
        return request.META.get(name) or None
