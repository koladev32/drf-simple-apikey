import pytest

from drf_simple_apikey.models import APIKey
from .fixtures.user import user
from .fixtures.api_key import active_api_key

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestApiKeyModel:
    pytestmark = pytest.mark.django_db

    def test_create_api_key(self, user):
        data = {
            "entity": user,
        }
        api_key, key = APIKey.objects.create_api_key(**data)

        assert type(key) is str

        assert api_key.entity.pk == user.pk
        assert not api_key.revoked
        assert api_key.expiry_date

    def test_get_api_key(self, active_api_key):
        api_key, _ = active_api_key

        api_key_pk = api_key.pk

        obj = APIKey.objects.get_api_key(api_key_pk)
        assert obj

    def test_revoke_api_key(self, active_api_key):
        api_key, _ = active_api_key

        APIKey.objects.revoke_api_key(api_key.pk)

        api_key.refresh_from_db()

        assert api_key.revoked


@pytest.mark.django_db
class TestApiKeyModelScopes:
    pytestmark = pytest.mark.django_db

    def test_has_scopes_with_no_scopes_configured_is_unrestricted(self, active_api_key):
        api_key, _ = active_api_key

        assert api_key.has_scopes(["fruits:read"])

    def test_has_scopes_with_no_required_scopes_is_always_true(self, active_api_key):
        api_key, _ = active_api_key
        api_key.scopes = ["fruits:read"]

        assert api_key.has_scopes([])

    def test_has_scopes_returns_true_when_all_required_scopes_are_granted(
        self, active_api_key
    ):
        api_key, _ = active_api_key
        api_key.scopes = ["fruits:read", "fruits:write"]

        assert api_key.has_scopes(["fruits:read"])

    def test_has_scopes_returns_false_when_a_required_scope_is_missing(
        self, active_api_key
    ):
        api_key, _ = active_api_key
        api_key.scopes = ["fruits:read"]

        assert not api_key.has_scopes(["fruits:write"])
