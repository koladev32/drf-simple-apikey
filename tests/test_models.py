import pytest

from rest_framework_simple_api_key.models import APIKey
from .fixtures.user import user

pytestmark = pytest.mark.django_dbs


@pytest.mark.django_db
class TestApiKeyModel:
    pytestmark = pytest.mark.django_db

    def test_api_keys_created(self, user):
        data = {
            "entity": user,
        }
        api_key, key = APIKey.objects.create_key(**data)

        assert type(key) is str

        assert api_key.entity.pk == user.pk
        assert not api_key.revoked
        assert api_key.expiry_date

    def test_get_key(self):
        pass

    def test_create_key(self):
        pass

    def test_revoke_keys(self):
        pass
