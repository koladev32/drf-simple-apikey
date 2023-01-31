import typing
from datetime import timedelta, datetime

from django.conf import settings
from django.db import models

from rest_framework_simple_api_key.crypto import ApiKeyCrypto
from rest_framework_simple_api_key.settings import package_settings


def _expiry_date():
    return datetime.now() + timedelta(settings.SIMPLE_API_KEY["API_KEY_LIFETIME"])


class APIKeyManager(models.Manager):
    key_crypto = ApiKeyCrypto()

    def get_key(self, pk: int | str):
        return self.get(revoked=False, pk=pk)

    def assign_key(self, obj) -> str:
        payload = {"_pk": obj.pk, "_exp": obj.expiry_date.timestamp()}
        key = self.key_crypto.generate(payload)

        return key

    def create_key(self, **kwargs: typing.Any) -> typing.Tuple[typing.Any, str]:
        # Prevent from manually setting the primary key.
        obj = self.model(**kwargs)
        obj.save()
        key = self.assign_key(obj)

        return obj, key

    def revoke_api_keys(self, pk: int | str):
        api_key = self.get_key(pk)

        api_key.revoked = True
        api_key.save()


class APIKey(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    entity = models.ForeignKey(
        settings.SIMPLE_API_KEY["AUTHENTICATION_MODEL"],
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    expiry_date = models.DateTimeField(
        default=_expiry_date,
        verbose_name="Expires",
        help_text="Once API key expires, entities cannot use it anymore.",
    )
    revoked = models.BooleanField(
        blank=True,
        default=False,
        help_text=(
            "If the API key is revoked, entities cannot use it anymore. "
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
