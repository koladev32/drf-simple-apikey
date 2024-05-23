import json
import os

import pytest

from drf_simple_apikey.crypto import ApiCrypto
from drf_simple_apikey.mutli_api_crypto import MultiApiCrypto


@pytest.mark.django_db
class TestCryptoFunctions:
    @pytest.fixture(scope="class")
    def key_crypto(self):
        from drf_simple_apikey.crypto import get_crypto

        return get_crypto()

    def test_encryption_and_decryption(self, key_crypto):
        payload = {"test": "data"}
        encrypted = key_crypto.encrypt(json.dumps(payload))
        decrypted = key_crypto.decrypt(encrypted)
        assert decrypted == payload

    def test_api_key_generation(self, key_crypto):
        payload = {"test": "data"}
        api_key = key_crypto.generate(payload)
        decrypted = key_crypto.decrypt(api_key)
        assert decrypted["_exp"]
        decrypted.pop("_exp")
        assert decrypted == payload

    def test_get_crypto_without_rotation_module(self, key_crypto):
        if not os.environ.get("TEST_WITH_ROTATION"):
            assert isinstance(key_crypto, ApiCrypto)

    def test_get_crypto_with_rotation_module(self, key_crypto):
        # You may need to mock the get_rotation_status and MultiApiCrypto as well for this test.
        # Replace the below class with whatever you expect when the rotation module is enabled.
        if os.environ.get("TEST_WITH_ROTATION"):
            assert isinstance(key_crypto, MultiApiCrypto)
