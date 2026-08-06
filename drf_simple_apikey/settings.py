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
    "IP_ADDRESS_HEADER": "REMOTE_ADDR",
    "IGNORED_ROUTES": ["/admin/"],  # Routes that should be ignored by API key authentication
    "ENFORCE_HTTPS": None,  # None means auto-detect: True when DEBUG=False, False when DEBUG=True
    "ENABLE_AUDIT_LOGGING": True,
    "MAX_ENDPOINTS_PER_KEY": 1000,
    "MAX_ENDPOINT_LENGTH": 500,
    "ENABLE_PER_KEY_SECRET": False,  # Opt-in defense-in-depth; see Threat Model docs
}

REMOVED_SETTINGS = ()


class PackageSettings(_APISettings):
    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "DRF_API_KEY", {})
        return self._user_settings

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://drf-api-key.koladev.xyz/docs/settings"

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
    # Reload in place (matching DRF's own APISettings.reload()) rather than
    # rebinding the module-level `package_settings` name to a new object:
    # every other module does `from drf_simple_apikey.settings import
    # package_settings`, which copies a reference to *this* object into
    # their own namespace. Rebinding the name here would only update this
    # module's reference, leaving everyone else holding a stale settings
    # snapshot from before the change.
    if kwargs["setting"] == "DRF_API_KEY":
        package_settings.reload()


setting_changed.connect(reload_api_settings)
