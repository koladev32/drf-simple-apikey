import pytest

from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

from rest_framework_simple_api_key.models import APIKey
from rest_framework_simple_api_key.backends import APIKeyAuthentication
from rest_framework_simple_api_key.settings import package_settings


@pytest.mark.django_db
class TestApiKeyAuthentication:
    pytestmark = pytest.mark.django_db

    def __init__(self, user):
        self.api_key_authentication = APIKeyAuthentication()
        self.factory = APIRequestFactory()
        authentication_keyword_header = package_settings.AUTHENTICATION_KEYWORD_HEADER

        data = {
            "entity": user,
        }
        api_key, key = APIKey.objects.create_key(**data)

        self.valid_request = self.factory.get('/test-request/',
                                              HTTP_AUTHORIZATION=f"{authentication_keyword_header} {key}")

        self.invalid_request = self.factory.get('/test-request/')

    def test_get_key(self, user):
        key = self.api_key_authentication.get_key(self.valid_request)
        assert type(key) is str

    def test_authenticate_valid(self):
        entity = self.api_key_authentication.authenticate(self.valid_request)

        assert isinstance(entity, User)

    def test_authenticate_invalid(self):
        entity = self.api_key_authentication.authenticate(self.valid_request)

        assert entity is None
