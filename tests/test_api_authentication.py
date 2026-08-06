import base64

import pytest

from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.test import APIRequestFactory

from drf_simple_apikey.backends import APIKeyAuthentication
from drf_simple_apikey.settings import package_settings

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
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.fixture
def invalid_request_with_revoked_api_key(user, revoked_api_key):
    factory = APIRequestFactory()
    _, key = revoked_api_key

    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.fixture
def valid_request(user, active_api_key):
    factory = APIRequestFactory()

    _, key = active_api_key
    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


def api_key_authentication():
    from drf_simple_apikey.backends import APIKeyAuthentication

    return APIKeyAuthentication()


def test_api_key_authentication_is_a_drf_auth_class():
    assert issubclass(APIKeyAuthentication, BaseAuthentication)


@pytest.mark.django_db
class TestApiKeyAuthentication:
    pytestmark = pytest.mark.django_db

    def test_get_key(self, valid_request):
        key = api_key_authentication().get_key(valid_request)
        assert type(key) is str

    def test_authenticate_valid_request(self, valid_request):
        entity, _ = api_key_authentication().authenticate(valid_request)

        assert isinstance(entity, User)

    def test_authenticate_request_without_authorization_header_returns_none(
        self, invalid_request
    ):
        # No Authorization header at all means this isn't an attempt to use
        # this scheme: DRF expects None here so it can try the next
        # authentication class instead of the request failing outright.
        assert api_key_authentication().authenticate(invalid_request) is None

    def test_authenticate_request_with_different_auth_scheme_returns_none(self, user):
        factory = APIRequestFactory()
        request = factory.get(
            "/test-request/", HTTP_AUTHORIZATION="Bearer some-other-token"
        )

        assert api_key_authentication().authenticate(request) is None

    def test_authenticate_request_with_matching_keyword_but_no_key_raises(self, user):
        factory = APIRequestFactory()
        request = factory.get(
            "/test-request/",
            HTTP_AUTHORIZATION=package_settings.AUTHENTICATION_KEYWORD_HEADER,
        )

        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"Incorrect API KEY format.",
        ):
            api_key_authentication().authenticate(request)

    def test_authenticate_invalid_request_with_expired_key(
        self, invalid_request_with_expired_api_key
    ):
        entity = None
        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"API Key has already expired.",
        ):
            entity, _ = api_key_authentication().authenticate(
                invalid_request_with_expired_api_key
            )

        assert entity is None

    def test_authenticate_invalid_request_with_revoked_key(
        self, invalid_request_with_revoked_api_key
    ):
        entity = None
        with pytest.raises(
            exceptions.AuthenticationFailed,
            match=r"This API Key has been revoked.",
        ):
            entity, _ = api_key_authentication().authenticate(
                invalid_request_with_revoked_api_key
            )

        assert entity is None


@api_view()
@authentication_classes([APIKeyAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def multi_auth_view(request):
    return Response({"username": request.user.username})


@pytest.mark.django_db
class TestMultiAuthenticatorFallback:
    pytestmark = pytest.mark.django_db

    def test_falls_back_to_basic_auth_when_no_api_key_header_is_sent(self, user):
        # Regression test: APIKeyAuthentication used to raise NotAuthenticated
        # whenever no Api-Key header was present, which stopped DRF from
        # trying any other authenticator listed after it. Combining it with
        # another authentication class (here, BasicAuthentication) must work.
        factory = APIRequestFactory()
        credentials = base64.b64encode(b"narutos:12345").decode()
        request = factory.get("/multi-auth/", HTTP_AUTHORIZATION=f"Basic {credentials}")

        response = multi_auth_view(request)

        assert response.status_code == 200
        assert response.data["username"] == "narutos"

    def test_rejects_when_neither_authenticator_matches(self):
        factory = APIRequestFactory()
        request = factory.get("/multi-auth/")

        response = multi_auth_view(request)

        assert response.status_code == 403
