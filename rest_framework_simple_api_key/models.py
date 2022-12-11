from datetime import timedelta, datetime

from django.db import models

from rest_framework_simple_api_key.settings import api_settings


def _expiry_date():
    return datetime.now() + timedelta(days=360)


class APIKeyManager(models.Manager):
    key_handler = ApiKeyHandler()

    def get_usable_key(self):
        pass

    def assign_key(self):
        pass

    def create_key(self):
        pass

    def revoke_api_keys(self):
        pass


class APIKey(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    entity = models.ForeignKey(
        api_settings.AUTHENTICATION_MODEL,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    expiry_date = models.DateTimeField(
        default=_expiry_date,
        verbose_name="Expires",
        help_text="Once API key expires, clients cannot use it anymore.",
    )
    revoked = models.BooleanField(
        blank=True,
        default=False,
        help_text=(
            "If the API key is revoked, clients cannot use it anymore. "
            "(This cannot be undone.)"
        ),
    )

    objects = APIKeyManager()

    def _has_expired(self) -> bool:
        if self.expiry_date is None:
            return False
        return self.expiry_date < datetime.now()

    _has_expired.short_description = "Has expired"
    _has_expired.boolean = True
    has_expired = property(_has_expired)
