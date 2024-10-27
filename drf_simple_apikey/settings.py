from datetime import timedelta

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

USER_SETTINGS = getattr(settings, "DRF_API_KEY", None)

DEFAULTS = {
    "FERNET_SECRET": "",
    "ROTATION_FERNET_SECRET": "",
    "API_KEY_LIFETIME": 365,
    "AUTHENTICATION_KEYWORD_HEADER": "Api-Key",
    "ROTATION_PERIOD": timedelta(days=7),
    "API_KEY_CLASS": "drf_simple_apikey.Apikey",
}

REMOVED_SETTINGS = ()


class PackageSettings(_APISettings):
    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "DRF_API_KEY", {})
        return self._user_settings

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://djangorestframework-simple-apikey.readthedocs.io/en/latest/settings.html"

        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    format_lazy(
                        _(
                            "The '{}' setting has been removed. Please refer to '{}' for available settings."
                        ),
                        setting,
                        SETTINGS_DOC,
                    )
                )

        return user_settings


package_settings = PackageSettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    global package_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "DRF_API_KEY":
        package_settings = PackageSettings(value, DEFAULTS)


setting_changed.connect(reload_api_settings)
