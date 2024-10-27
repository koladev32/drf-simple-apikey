import pytest
from django.contrib.admin import site
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.test import RequestFactory

from drf_simple_apikey.admin import ApiKeyAdmin
from drf_simple_apikey.models import APIKey

from .fixtures.user import user


def build_admin_request(rf: RequestFactory) -> HttpRequest:
    request = rf.post("/")

    def get_response(request: HttpRequest) -> HttpResponse:
        raise NotImplementedError  # pragma: no cover  # Unused in these tests.

    # NOTE: all middleware must be instantiated before
    # any middleware can process the request.
    sessions = SessionMiddleware(get_response)
    messages = MessageMiddleware(sessions.get_response)

    sessions.process_request(request)
    messages.process_request(request)

    return request


@pytest.mark.django_db
def test_admin_readonly_fields(rf: RequestFactory, user) -> None:
    request = build_admin_request(rf)

    admin = ApiKeyAdmin(APIKey, site)

    assert admin.get_readonly_fields(request) == (
        "entity",
        "created",
    )

    api_key = APIKey(name="test", entity=user)
    assert admin.get_readonly_fields(request, obj=api_key) == (
        "entity",
        "created",
    )

    api_key = APIKey(name="test", entity=user, revoked=True)
    assert admin.get_readonly_fields(request, obj=api_key) == (
        "entity",
        "created",
        "name",
        "revoked",
        "expiry_date",
        "whitelisted_ips",
        "blacklisted_ips",
    )


@pytest.mark.django_db
def test_admin_create_api_key(rf: RequestFactory, user) -> None:
    request = build_admin_request(rf)

    admin = ApiKeyAdmin(APIKey, site)
    api_key = APIKey(name="test", entity=user)

    assert not api_key.pk
    admin.save_model(request, obj=api_key)
    assert api_key.pk

    messages = get_messages(request)
    assert len(messages) == 1


@pytest.mark.django_db
def test_admin_update_api_key(rf: RequestFactory, user) -> None:
    request = build_admin_request(rf)

    admin = ApiKeyAdmin(APIKey, site)
    api_key, _ = APIKey.objects.create_api_key(name="test", entity=user)

    api_key.name = "another-test"
    admin.save_model(request, obj=api_key)
    refreshed = APIKey.objects.get(pk=api_key.pk)
    assert refreshed.name == "another-test"
