import pytest

pytestmark = pytest.mark.django_dbs


@pytest.mark.django_db
class TestApiKeyModel:
    pytestmark = pytest.mark.django_db

    def test_api_keys_created(self):
        pass

    def test_get_key(self):
        pass

    def test_create_key(self):
        pass

    def test_revoke_keys(self):
        pass
