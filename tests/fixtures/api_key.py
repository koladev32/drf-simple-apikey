import pytest
from django.utils.timezone import now

from rest_framework_simple_api_key.models import APIKey
from .user import user, inactive_user


@pytest.fixture
def inactive_entity_api_key(inactive_user):
    data = {
        "entity": inactive_user,
    }
    return APIKey.objects.create_api_key(
        **data
    )  # This will return api_key:object, key:string@pytest.fixture


@pytest.fixture
def active_api_key(user):
    data = {
        "entity": user,
    }
    return APIKey.objects.create_api_key(
        **data
    )  # This will return api_key:object, key:string@pytest.fixture


@pytest.fixture
def active_only_api_key(user):
    data = {
        "entity": user,
    }
    apikey, _ = APIKey.objects.create_api_key(
        **data
    )  # This will return api_key:object

    return apikey


@pytest.fixture
def expired_api_key(user):
    data = {"entity": user, "expiry_date": now()}
    return APIKey.objects.create_api_key(
        **data
    )  # This will return api_key:object, key:string


@pytest.fixture
def revoked_api_key(user):
    data = {"entity": user, "revoked": True}
    return APIKey.objects.create_api_key(
        **data
    )  # This will return api_key:object, key:string
