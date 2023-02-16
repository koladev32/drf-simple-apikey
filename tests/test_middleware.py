import pytest

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework_simple_api_key.settings import package_settings

from .fixtures.api_key import active_api_key
from .fixtures.user import user


@pytest.mark.django_db
class TestApiKeyMiddleware:

    def test_custom_request_attribute(self, active_api_key):
        client = APIClient()
        _, api_key = active_api_key

        client.credentials(HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {api_key}")

        response = client.get(reverse("test-request"))
        request = response.wsgi_request

        assert request.user
        assert request.organization
        assert request.user == request.organization
        assert isinstance(request.organization, User)
        assert isinstance(request.user, User)
