from datetime import timedelta

import pytest
from django.utils.timezone import now

from rest_framework_simple_api_key.models import APIKey
from .user import user


@pytest.fixture
def active_api_key(user):
    data = {
        "entity": user,
    }
    return APIKey.objects.create_key(
        **data
    )  # This will return api_key:object, key:string@pytest.fixture


@pytest.fixture
def expired_api_key(user):
    data = {"entity": user, "expiry_date": now()}
    return APIKey.objects.create_key(
        **data
    )  # This will return api_key:object, key:string


@pytest.fixture
def revoked_api_key(user):
    data = {"entity": user, "revoked": True}
    return APIKey.objects.create_key(
        **data
    )  # This will return api_key:object, key:string
