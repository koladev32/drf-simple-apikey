import pytest

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.test import APIRequestFactory

from drf_simple_apikey.backends import APIKeyAuthentication
from drf_simple_apikey.permissions import IsActiveEntity
from drf_simple_apikey.settings import package_settings

from .fixtures.api_key import inactive_entity_api_key, active_api_key
from .fixtures.user import inactive_user, user

pytestmark = pytest.mark.django_db


@api_view()
@authentication_classes([APIKeyAuthentication])
@permission_classes([IsActiveEntity])
def view(request: Request) -> Response:
    return Response()


@pytest.fixture
def request_with_inactive_entity(inactive_user, inactive_entity_api_key):
    factory = APIRequestFactory()

    _, key = inactive_entity_api_key
    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.fixture
def request_with_active_entity(user, active_api_key):
    factory = APIRequestFactory()

    _, key = active_api_key
    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


@pytest.mark.django_db
class TestApiKeyPermissions:
    pytestmark = pytest.mark.django_db

    def test_if_inactive_user_does_not_have_permissions(
        self, request_with_inactive_entity
    ):
        response = view(request_with_inactive_entity)

        assert response.status_code == 403

    def test_if_active_user_does_have_permissions(self, request_with_active_entity):
        response = view(request_with_active_entity)

        assert response.status_code == 200
