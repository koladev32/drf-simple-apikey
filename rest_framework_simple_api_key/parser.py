import typing

from django.http import HttpRequest
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed

from rest_framework_simple_api_key.settings import package_settings


class APIKeyParser:
    keyword = package_settings.AUTHENTICATION_KEYWORD_HEADER
    message = "No API KEY provided."

    def get(self, request: HttpRequest) -> typing.Optional[str]:
        api_key_header = getattr(package_settings, "API_KEY_HEADER", None)

        if api_key_header is not None:
            return self.get_from_header(request, api_key_header)

        return self.get_from_authorization(request)

    def get_from_authorization(self, request: HttpRequest) -> typing.Optional[str]:
        authorization = request.META.get("HTTP_AUTHORIZATION")

        if not authorization:
            raise NotAuthenticated

        try:
            _, key = authorization.split(f"{self.keyword} ")
        except ValueError:
            raise AuthenticationFailed("Incorrect API KEY format.")

        return key

    def get_from_header(self, request: HttpRequest, name: str) -> typing.Optional[str]:
        return request.META.get(name) or None
