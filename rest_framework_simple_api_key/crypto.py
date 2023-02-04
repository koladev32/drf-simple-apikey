"""
This modules provides the `ApiKeyCrypto` class that contains
methods needed to generate, encrypt, and decrypt an API Key.
"""
import json
from copy import copy
from datetime import timedelta

from cryptography.fernet import Fernet
from django.conf import settings

from django.utils.timezone import now


class ApiKeyCrypto:
    def __init__(self):
        """
        We first start by making some checks on the fernet secret to ensure the value is not empty.
        """
        fernet_key, api_key_lifetime = settings.SIMPLE_API_KEY.get(
            "FERNET_SECRET"
        ), settings.SIMPLE_API_KEY.get("API_KEY_LIFETIME")

        if fernet_key is None or fernet_key == "":
            raise KeyError("A fernet secret is not defined in the Django settings.")

        self.fernet = fernet_key
        self.api_key_lifetime = api_key_lifetime

    def encrypt(self, payload: str) -> str:
        """
        :param payload: str
        :return: key: str
        """
        return self.fernet.encrypt(payload.encode()).decode()

    def decrypt(self, key: str) -> dict:
        """
        :param key: representing the api key
        :return: a dict with the decrypted data
        """
        data = self.fernet.decrypt(key.encode()).decode()

        return json.loads(data)

    def generate(self, payload: dict) -> str:
        """
        :param payload: a dict representing the data to encrypt.
        :return: a generated key using the `encrypt` method.
        """
        expires_at = now() + timedelta(days=self.api_key_lifetime)
        data = copy(payload)

        data["_exp"] = (
            expires_at.timestamp() if data.get("_exp") is None else data["_exp"]
        )

        api_key = self.encrypt(json.dumps(data))
        return api_key
