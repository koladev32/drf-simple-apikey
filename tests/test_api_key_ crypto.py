import pytest
import datetime
from rest_framework_simple_api_key.crypto import ApiKeyCrypto


class TestApiCrypto:

    key_crypto = ApiKeyCrypto()
    payload = {
            "user_id": 1,
            "_exp": datetime.datetime.now()
        }

    def test_generate_keys(self):
        key = self.key_crypto.generate(self.payload)

        assert type(key) is type(str)

    def test_encode(self):
        key_encoded = self.key_crypto.encode(self.payload)

        assert type(key_encoded) is type(str)

    def test_decode(self):

        # Encoding key

        key_encoded = self.key_crypto.encode(self.payload)

        # Decoding key

        key_decoded = self.key_crypto.decode(key_encoded)

        assert type(key_decoded) is type(dict)

        assert key_decoded['user_id'] == self.payload['user_id']
        assert key_decoded['_exp'] == self.payload['_exp']
