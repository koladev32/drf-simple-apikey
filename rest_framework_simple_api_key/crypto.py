"""
This modules provides the `ApiKeyCrypto` classes that contain
methods needed to generate, encrypt, and decrypt an API Key.
"""
import json
from copy import copy
from datetime import timedelta

from cryptography.fernet import Fernet
from django.conf import settings

from django.utils.timezone import now

from rest_framework_simple_api_key.settings import package_settings


class BaseApiCrypto:
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


class ApiCrypto(BaseApiCrypto):
    def __init__(self):
        fernet_key, api_key_lifetime = (
            package_settings.FERNET_SECRET,
            package_settings.API_KEY_LIFETIME,
        )

        if fernet_key is None or fernet_key == "":
            raise KeyError("A fernet secret is not defined in the Django settings.")

        self.fernet = Fernet(fernet_key)
        self.api_key_lifetime = api_key_lifetime


def get_crypto():
    if "rest_framework_simple_api_key.rotation" in settings.INSTALLED_APPS:
        try:
            # Try to import necessary components and initialize the MultiApiCrypto.
            # This might fail if certain conditions aren't met, like missing migrations.
            from rest_framework_simple_api_key.rotation.utils import get_rotation_status
            from .mutli_api_crypto import MultiApiCrypto

            if get_rotation_status():
                return MultiApiCrypto()
        except Exception as e:
            print(f"Error initializing MultiApiCrypto: {e}")
            raise e

    # If the rotation module isn't installed, or if there was an error initializing MultiApiCrypto,
    # fall back to returning an instance of the standard ApiCrypto.
    return ApiCrypto()
