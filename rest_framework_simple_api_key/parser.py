from django.http import HttpRequest
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed

from rest_framework_simple_api_key.settings import package_settings


class APIKeyParser:
    keyword = package_settings.AUTHENTICATION_KEYWORD_HEADER
    message = "No API KEY provided."

    def get(self, request: HttpRequest):
        api_key_header = getattr(package_settings, "API_KEY_HEADER", None)

        if api_key_header is not None:
            return self.get_from_header(request, api_key_header)

        return self.get_from_authorization(request)

    def get_from_authorization(self, request: HttpRequest):
        authorization = request.META.get("HTTP_AUTHORIZATION")

        if not authorization:
            raise NotAuthenticated

        try:
            _, key = authorization.split("{} ".format(self.keyword))
        except ValueError:
            raise AuthenticationFailed

        return key

    def get_from_header(self, request: HttpRequest, name: str):
        return request.META.get(name) or None
