import pytest
from django.conf import settings

from django.contrib.auth.models import User
from rest_framework import exceptions

from rest_framework.test import APIRequestFactory

from rest_framework_simple_api_key.backends import APIKeyAuthentication

from .fixtures.user import user
from .fixtures.api_key import expired_api_key, active_api_key, revoked_api_key

pytestmark = pytest.mark.django_db


@pytest.fixture
def invalid_request(user):
    factory = APIRequestFactory()

    return factory.get("/test-request/")


@pytest.fixture
def invalid_request_with_expired_api_key(user, expired_api_key):
    factory = APIRequestFactory()
    _, key = expired_api_key

    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{settings.SIMPLE_API_KEY['AUTHENTICATION_KEYWORD_HEADER']} {key}",
    )


@pytest.fixture
def invalid_request_with_revoked_api_key(user, revoked_api_key):
    factory = APIRequestFactory()
    _, key = revoked_api_key

    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{settings.SIMPLE_API_KEY['AUTHENTICATION_KEYWORD_HEADER']} {key}",
    )


@pytest.fixture
def valid_request(user, active_api_key):
    factory = APIRequestFactory()

    _, key = active_api_key
    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{settings.SIMPLE_API_KEY['AUTHENTICATION_KEYWORD_HEADER']} {key}",
    )


@pytest.mark.django_db
class TestApiKeyAuthentication:
    pytestmark = pytest.mark.django_db

    api_key_authentication = APIKeyAuthentication()

    def test_get_key(self, valid_request):
        key = self.api_key_authentication.get_key(valid_request)
        assert type(key) is str

    def test_authenticate_valid(self, valid_request):
        entity, _ = self.api_key_authentication.authenticate(valid_request)

        assert isinstance(entity, User)

    def test_authenticate_invalid(self, invalid_request):
        entity = None
        with pytest.raises(
            exceptions.NotAuthenticated,
            match=r"Authentication credentials were not provided.",
        ):
            entity, _ = self.api_key_authentication.authenticate(invalid_request)

        assert entity is None

    def test_authenticate_invalid_with_expired_key(
        self, invalid_request_with_expired_api_key
    ):
        entity = None
        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"API Key has already expired.",
        ):
            entity, _ = self.api_key_authentication.authenticate(
                invalid_request_with_expired_api_key
            )

        assert entity is None

    def test_authenticate_invalid_with_revoked_key(
        self, invalid_request_with_revoked_api_key
    ):
        entity = None
        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"This API Key has been revoked.",
        ):
            entity, _ = self.api_key_authentication.authenticate(
                invalid_request_with_revoked_api_key
            )

        assert entity is None