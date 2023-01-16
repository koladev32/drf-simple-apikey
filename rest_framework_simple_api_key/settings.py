from datetime import timedelta

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

USER_SETTINGS = getattr(settings, "SIMPLE_API_KEY", None)

DEFAULTS = {"FERNET_SECRET": "", "API_KEY_LIFETIME": timedelta(days=365)}

REMOVED_SETTINGS = (
    "AUTH_HEADER_TYPE",
    "AUTH_TOKEN_CLASS",
    "SECRET_KEY",
    "TOKEN_BACKEND_CLASS",
)


class APISettings(_APISettings):
    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://django-rest-framework-simple-apikey.readthedocs.io/en/latest/settings.html"

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


api_settings = APISettings(DEFAULTS, USER_SETTINGS)


def reload_api_settings(*args, **kwargs):
    global api_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "SIMPLE_API_KEY":
        api_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_api_settings)
