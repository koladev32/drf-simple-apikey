import typing

from django.http import HttpRequest
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed

from rest_framework_simple_api_key.settings import package_settings


class APIKeyParser:
    """
    This is a custom parser used to retrieve the API Key from the
    authorization header. You can add custom parsing validation here.
    """

    keyword = package_settings.AUTHENTICATION_KEYWORD_HEADER
    message = "No API key provided."

    def get(self, request: HttpRequest) -> typing.Optional[str]:
        return self.get_from_authorization(request)

    def get_from_authorization(self, request: HttpRequest) -> typing.Optional[str]:
        authorization = request.META.get("HTTP_AUTHORIZATION")

        if not authorization:
            raise NotAuthenticated(self.message)

        try:
            _, key = authorization.split(f"{self.keyword} ")
        except ValueError:
            raise AuthenticationFailed("Incorrect API KEY format.")

        return key

    def get_from_header(self, request: HttpRequest, name: str) -> typing.Optional[str]:
        return request.META.get(name) or None
