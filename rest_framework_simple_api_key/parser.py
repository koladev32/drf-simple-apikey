import typing

from django.conf import settings
from django.http import HttpRequest
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed


class APIKeyParser:
    """
    This is a custom parser used to retrieve the API Key from the
    authorization header. You can add custom parsing validation here.
    """

    keyword = settings.SIMPLE_API_KEY.get("AUTHENTICATION_KEYWORD_HEADER")
    message = "No API key provided."

    def get(self, request: HttpRequest) -> typing.Optional[str]:
        api_key_header = settings.SIMPLE_API_KEY.get("API_KEY_HEADER")

        if api_key_header is not None:
            return self.get_from_header(request, api_key_header)

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
