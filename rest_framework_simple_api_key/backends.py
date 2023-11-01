import typing

from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import exceptions


from rest_framework_simple_api_key.crypto import get_crypto
from rest_framework_simple_api_key.models import APIKey
from rest_framework_simple_api_key.parser import APIKeyParser


class APIKeyAuthentication(BaseBackend):
    model = APIKey
    key_parser = APIKeyParser()

    def __init__(self):
        self.key_crypto = get_crypto()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        return self.key_parser.get(request)

    def authenticate(self, request, **kwargs):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires api key authentication.
        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
        this means we know authentication will fail. An example of
        this is when the request does not include an api key in the
        headers.

        2) `(entity)` - We return an entity object when
        authentication is successful.
        If neither case is met, that means there's an error,
        and we do not return anything.
        We simply raise the `AuthenticationFailed`
        exception and let Django REST Framework
        handle the rest.
        """

        key = self.get_key(request)

        return self._authenticate_credentials(request, key)

    def _authenticate_credentials(self, request, key):
        key_crypto = self.key_crypto

        try:
            payload = key_crypto.decrypt(key)
        except ValueError:
            raise exceptions.AuthenticationFailed("Invalid API Key.")

        if "_pk" not in payload or "_exp" not in payload:
            raise exceptions.AuthenticationFailed("Invalid API Key.")

        if payload["_exp"] < now().timestamp():
            raise exceptions.AuthenticationFailed("API Key has already expired.")
        try:
            api_key = self.model.objects.get(id=payload["_pk"])
        except ObjectDoesNotExist:  # pylint: disable=maybe-no-member
            raise exceptions.AuthenticationFailed("No entity matching this api key.")

        if api_key.revoked:
            raise exceptions.AuthenticationFailed("This API Key has been revoked.")

        return api_key.entity, key

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass
