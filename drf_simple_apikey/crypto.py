"""
This modules provides the `ApiKeyCrypto` classes that contain
methods needed to generate, encrypt, and decrypt an API Key.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import re
from copy import copy
from datetime import timedelta

from cryptography.fernet import Fernet
from django.conf import settings

from django.utils.timezone import now

from drf_simple_apikey.settings import package_settings

logger = logging.getLogger(__name__)


def _validate_fernet_key(fernet_key: str) -> tuple[bool, list[str]]:
    """
    Validate Fernet key format and security.
    Returns (is_valid, warnings_list).
    """
    warnings = []

    # Check if key is empty
    if not fernet_key or fernet_key.strip() == "":
        return False, ["Fernet key is empty"]

    # Check key format (base64, 32 bytes when decoded)
    try:
        decoded = base64.urlsafe_b64decode(fernet_key)
        if len(decoded) != 32:
            return False, [f"Fernet key must be 32 bytes when decoded, got {len(decoded)}"]
    except Exception as e:
        return False, [f"Invalid Fernet key format: {str(e)}"]

    # Check for weak patterns (all same character, sequential, etc.)
    if len(set(decoded)) < 4:
        warnings.append("Fernet key appears to have low entropy (weak pattern detected)")

    # Check if key appears to be hardcoded (common patterns)
    # This is a heuristic check - look for keys in common locations
    if not os.getenv("FERNET_SECRET") and not os.getenv("DRF_API_KEY_FERNET_SECRET"):
        # Check if key looks like it might be in source code
        # (This is a simple heuristic - keys from env vars usually look random)
        if re.match(r"^[A-Za-z0-9+/=]{43}$", fernet_key):
            # Check if it's a common example/test key pattern
            common_patterns = [
                "test",
                "example",
                "demo",
                "default",
                "changeme",
                "secret",
            ]
            key_lower = fernet_key.lower()
            if any(pattern in key_lower for pattern in common_patterns):
                warnings.append(
                    "Fernet key appears to contain common words - may be insecure"
                )
            else:
                warnings.append(
                    "Fernet key not found in environment variables - ensure it's not hardcoded"
                )

    return True, warnings


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
    def __init__(self) -> None:
        fernet_key, api_key_lifetime = (
            package_settings.FERNET_SECRET,
            package_settings.API_KEY_LIFETIME,
        )

        if fernet_key is None or fernet_key == "":
            raise KeyError("A fernet secret is not defined in the Django settings.")

        # Validate Fernet key
        is_valid, warnings = _validate_fernet_key(fernet_key)
        if not is_valid:
            raise ValueError(f"Invalid Fernet key: {', '.join(warnings)}")

        # Log warnings if any
        for warning in warnings:
            logger.warning(f"Fernet key security warning: {warning}")

        try:
            self.fernet = Fernet(fernet_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Fernet with provided key: {str(e)}")

        self.api_key_lifetime = api_key_lifetime


def get_crypto() -> BaseApiCrypto:
    if "drf_simple_apikey.rotation" in settings.INSTALLED_APPS:
        try:
            # Try to import necessary components and initialize the MultiApiCrypto.
            # This might fail if certain conditions aren't met, like missing migrations.
            from drf_simple_apikey.rotation.utils import get_rotation_status
            from .mutli_api_crypto import MultiApiCrypto

            if get_rotation_status():
                return MultiApiCrypto()
        except Exception as e:
            # Use proper logging instead of print
            logger.error(
                "Error initializing MultiApiCrypto",
                extra={"error": str(e)},
                exc_info=True,
            )
            raise

    # If the rotation module isn't installed, or if there was an error initializing MultiApiCrypto,
    # fall back to returning an instance of the standard ApiCrypto.
    return ApiCrypto()
