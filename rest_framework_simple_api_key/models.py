import typing
from datetime import timedelta, datetime

from django.conf import settings
from django.db import models

from rest_framework_simple_api_key.crypto import get_crypto
from rest_framework_simple_api_key.settings import package_settings


def _expiry_date():
    return datetime.now() + timedelta(package_settings.API_KEY_LIFETIME)


class AbstractAPIKeyManager(models.Manager):
    def get_api_key(self, pk: int | str):
        return self.get(revoked=False, pk=pk)

    def assign_api_key(self, obj) -> str:
        payload = {"_pk": obj.pk, "_exp": obj.expiry_date.timestamp()}
        key = get_crypto().generate(payload)

        return key

    def create_api_key(self, **kwargs: typing.Any) -> typing.Tuple[typing.Any, str]:
        # Prevent from manually setting the primary key.
        obj = self.model(**kwargs)
        obj.save()
        key = self.assign_api_key(obj)

        return obj, key

    def revoke_api_key(self, pk: int | str):
        api_key = self.get_api_key(pk)

        api_key.revoked = True
        api_key.save()


class APIKeyManager(AbstractAPIKeyManager):
    pass


class AbstractAPIKey(models.Model):
    """
    Abstract API KEY model
    """

    name = models.CharField(max_length=255, null=True, blank=True)

    entity = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    created = models.DateTimeField(auto_now=True)

    objects = APIKeyManager()

    def _has_expired(self) -> bool:
        if self.expiry_date is None:
            return False
        return self.expiry_date < datetime.now()

    _has_expired.short_description = "Has expired"
    _has_expired.boolean = True
    has_expired = property(_has_expired)

    class Meta:
        abstract = True
        verbose_name = "API key"
        verbose_name_plural = "API keys"

    def __str__(self):
        return self.name


class APIKey(AbstractAPIKey):
    """
    API KEY model
    """

    pass
