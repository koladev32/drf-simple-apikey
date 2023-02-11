import pytest

from django.conf import settings
from rest_framework.test import APIRequestFactory

from rest_framework_simple_api_key.settings import package_settings

from .fixtures.api_key import active_api_key
from .fixtures.user import user


@pytest.mark.django_db
class TestApiKeyMiddleware:
    pytestmark = pytest.mark.django_db

    def test_custom_request_attribute(self, active_api_key):
        factory = APIRequestFactory()

        api_key, _ = active_api_key
        request = factory.get(
            "/test-request/",
            HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {api_key}",
        )
        assert hasattr(request, settings.SIMPLE_API_KEY["custom_entity_name"])
        assert request.entity
