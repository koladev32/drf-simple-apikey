import hashlib

import pytest
from rest_framework import exceptions
from rest_framework.test import APIRequestFactory

from drf_simple_apikey.backends import APIKeyAuthentication
from drf_simple_apikey.crypto import get_crypto
from drf_simple_apikey.models import APIKey
from drf_simple_apikey.settings import package_settings

from .fixtures.user import user

pytestmark = pytest.mark.django_db

FERNET_SECRET = "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA="
ROTATION_FERNET_SECRET = "EqkeOOgvV8bt70vUJiVXloNycn5bt_z1VqyoAi9K6f4="


def enable_per_key_secret(settings):
    # Keep ROTATION_FERNET_SECRET around too: overriding DRF_API_KEY
    # wholesale would otherwise drop it, breaking get_crypto() under
    # TEST_WITH_ROTATION=1 (MultiApiCrypto requires both secrets).
    settings.DRF_API_KEY = {
        "FERNET_SECRET": FERNET_SECRET,
        "ROTATION_FERNET_SECRET": ROTATION_FERNET_SECRET,
        "ENABLE_PER_KEY_SECRET": True,
    }


def authenticated_request(key):
    factory = APIRequestFactory()
    return factory.get(
        "/test-request/",
        HTTP_AUTHORIZATION=f"{package_settings.AUTHENTICATION_KEYWORD_HEADER} {key}",
    )


class TestPerKeySecretDisabledByDefault:
    def test_disabled_by_default(self):
        assert package_settings.ENABLE_PER_KEY_SECRET is False

    def test_key_creation_does_not_set_hashed_secret_by_default(self, user):
        api_key, _ = APIKey.objects.create_api_key(entity=user)

        assert api_key.hashed_secret == ""

    def test_forged_key_still_authenticates_when_feature_is_off(self, user):
        # Documents *existing* behavior: with the feature off (the
        # default), anyone holding just FERNET_SECRET can mint a key for an
        # existing row, exactly as before this change. This is not a
        # regression -- it's precisely what ENABLE_PER_KEY_SECRET protects
        # against once turned on, and turning it on is opt-in.
        api_key, _ = APIKey.objects.create_api_key(entity=user)
        forged = get_crypto().generate({"_pk": api_key.pk})

        entity, _ = APIKeyAuthentication().authenticate(authenticated_request(forged))

        assert entity == user


class TestPerKeySecretEnabled:
    def test_key_creation_stores_hashed_secret_and_embeds_raw_secret(
        self, user, settings
    ):
        enable_per_key_secret(settings)

        api_key, key = APIKey.objects.create_api_key(entity=user)
        api_key.refresh_from_db()

        assert api_key.hashed_secret != ""
        payload = get_crypto().decrypt(key)
        assert (
            hashlib.sha256(payload["_secret"].encode()).hexdigest()
            == api_key.hashed_secret
        )

    def test_legitimate_key_still_authenticates(self, user, settings):
        enable_per_key_secret(settings)

        _, key = APIKey.objects.create_api_key(entity=user)

        entity, _ = APIKeyAuthentication().authenticate(authenticated_request(key))

        assert entity == user

    def test_forged_key_without_matching_secret_is_rejected(self, user, settings):
        enable_per_key_secret(settings)

        # The actual regression test for #103: an attacker with only
        # FERNET_SECRET (no database access) can still encrypt a payload
        # referencing an existing row's pk, but without the per-key secret
        # it must now be rejected.
        api_key, _ = APIKey.objects.create_api_key(entity=user)
        forged = get_crypto().generate({"_pk": api_key.pk})

        with pytest.raises(exceptions.AuthenticationFailed, match=r"Invalid API Key."):
            APIKeyAuthentication().authenticate(authenticated_request(forged))

    def test_forged_key_with_wrong_secret_is_rejected(self, user, settings):
        enable_per_key_secret(settings)

        api_key, _ = APIKey.objects.create_api_key(entity=user)
        forged = get_crypto().generate({"_pk": api_key.pk, "_secret": "wrong-secret"})

        with pytest.raises(exceptions.AuthenticationFailed, match=r"Invalid API Key."):
            APIKeyAuthentication().authenticate(authenticated_request(forged))

    def test_pre_upgrade_key_without_hashed_secret_is_grandfathered_in(
        self, user, settings
    ):
        # Simulates a key issued before this feature existed (or before it
        # was enabled): the DB row has no hashed_secret, and the token
        # naturally has no _secret in its payload either. Enabling the
        # setting later must not break it.
        api_key = APIKey.objects.create(entity=user)
        assert api_key.hashed_secret == ""
        legacy_key = get_crypto().generate(
            {"_pk": api_key.pk, "_exp": api_key.expiry_date.timestamp()}
        )

        enable_per_key_secret(settings)

        entity, _ = APIKeyAuthentication().authenticate(
            authenticated_request(legacy_key)
        )

        assert entity == user
