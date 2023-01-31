import pytest

from rest_framework_simple_api_key.models import APIKey
from .user import user


@pytest.fixture
def active_api_key(user):
    data = {
        "entity": user,
    }
    return APIKey.objects.create_key(**data)  # This will return api_key:object, key:string
