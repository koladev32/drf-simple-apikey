from cryptography.fernet import MultiFernet, Fernet

from drf_simple_apikey.crypto import BaseApiCrypto
from drf_simple_apikey.settings import package_settings


class MultiApiCrypto(BaseApiCrypto):
    def __init__(self):
        fernet_key, rotation_fernet_key, api_key_lifetime = (
            package_settings.FERNET_SECRET,
            package_settings.ROTATION_FERNET_SECRET,
            package_settings.API_KEY_LIFETIME,
        )

        if (
            fernet_key is None
            or rotation_fernet_key is None
            or fernet_key == ""
            or rotation_fernet_key == ""
        ):
            raise KeyError(
                "Fernet secrets are not defined in the Django settings for rotation. Please, check again."
            )

        self.fernet = MultiFernet([Fernet(rotation_fernet_key), Fernet(fernet_key)])
        self.api_key_lifetime = api_key_lifetime
