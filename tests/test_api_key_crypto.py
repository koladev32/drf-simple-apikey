import json

import pytest


@pytest.mark.django_db
class TestApiCrypto:
    def __init__(self):
        from rest_framework_simple_api_key.crypto import get_crypto

        key_crypto = get_crypto()

    payload = {"user_id": 1}

    def _encode_payload(self):
        return json.dumps(self.payload)

    def test_generate_keys(self):
        key = self.key_crypto.generate(self.payload)

        assert type(key) is str

    def test_encrypt(self):
        key_encoded = self.key_crypto.encrypt(self._encode_payload())

        assert type(key_encoded) is str

    def test_decrypt(self):
        # Encoding key

        key_encoded = self.key_crypto.encrypt(self._encode_payload())

        # Decoding key

        key_decoded = self.key_crypto.decrypt(key_encoded)

        assert type(key_decoded) is dict

        assert key_decoded["user_id"] == self.payload["user_id"]
