from django.contrib.auth.backends import BaseBackend


from rest_framework_simple_api_key.crypto import ApiKeyCrypto
from rest_framework_simple_api_key.models import APIKey
from rest_framework_simple_api_key.parser import APIKeyParser


class APIKeyAuthentication(BaseBackend):
    model = APIKey
    key_parser = APIKeyParser()
    key_crypto = ApiKeyCrypto()

    def get_key(self):
        pass

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
        If neither case is met, that means there's an error
        and we do not return anything.
        We simple raise the `AuthenticationFailed`
        exception and let Django REST Framework
        handle the rest.
        """
        pass

    def _authenticate_credentials(self, request, key):
        pass

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass