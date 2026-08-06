from __future__ import annotations

import hashlib
import secrets
import typing
from datetime import timedelta, datetime

from django.conf import settings
from django.db import models

from drf_simple_apikey.crypto import get_crypto
from drf_simple_apikey.settings import package_settings


def _expiry_date() -> datetime:
    from django.utils import timezone
    return timezone.now() + timedelta(days=package_settings.API_KEY_LIFETIME)


class AbstractAPIKeyManager(models.Manager):
    def get_api_key(self, pk: int | str) -> "AbstractAPIKey":
        return self.get(revoked=False, pk=pk)

    def assign_api_key(self, obj: "AbstractAPIKey") -> str:
        payload = {"_pk": obj.pk, "_exp": obj.expiry_date.timestamp()}

        if package_settings.ENABLE_PER_KEY_SECRET:
            # Opt-in defense-in-depth: a random per-key secret, stored only
            # as a hash, so that a leaked FERNET_SECRET alone isn't enough
            # to forge a working key for an existing entity — the attacker
            # would also need this secret (or database access), since the
            # hash can't be reversed back into it. See the Threat Model
            # docs for the full rationale. Off by default so existing
            # setups and already-issued keys are unaffected; enabling it
            # only changes keys created from that point on.
            #
            # This intentionally uses a plain SHA-256 digest, not a
            # password hasher (PBKDF2/bcrypt/Argon2). Those are slow *on
            # purpose* to resist brute-forcing low-entropy human passwords
            # -- there's no such risk here, since the secret is a 256-bit
            # random token, not something guessable. Using a slow hasher
            # would add real per-request latency for no security benefit
            # against this threat model (see the PR description for
            # benchmarks), which conflicts with why this package uses
            # Fernet in the first place.
            secret = secrets.token_urlsafe(32)
            obj.hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
            obj.save(update_fields=["hashed_secret"])
            payload["_secret"] = secret

        key = get_crypto().generate(payload)

        return key

    def create_api_key(self, **kwargs: typing.Any) -> tuple[typing.Any, str]:
        # Prevent from manually setting the primary key.
        obj = self.model(**kwargs)
        obj.save()
        key = self.assign_api_key(obj)

        return obj, key

    def revoke_api_key(self, pk: int | str) -> None:
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

    whitelisted_ips = models.JSONField(
        blank=True,
        null=True,
        help_text="List of allowed IP addresses for this API key.",
    )
    blacklisted_ips = models.JSONField(
        blank=True,
        null=True,
        help_text="List of denied IP addresses for this API key.",
    )

    scopes = models.JSONField(
        blank=True,
        null=True,
        help_text=(
            "List of scopes granted to this API key (e.g. ['read', 'write']). "
            "Leave empty for unrestricted access."
        ),
    )

    hashed_secret = models.CharField(
        max_length=64,
        blank=True,
        default="",
        editable=False,
        help_text=(
            "SHA-256 hash of a random per-key secret embedded in the issued "
            "key, checked in addition to Fernet decryption succeeding. Only "
            "set when ENABLE_PER_KEY_SECRET is on. Empty for keys issued "
            "before this field existed or while the setting is off."
        ),
    )

    objects = APIKeyManager()

    def has_scopes(self, required_scopes: typing.Sequence[str]) -> bool:
        """
        Returns True if this API key is allowed to act with all the given
        `required_scopes`. A key with no scopes configured is unrestricted
        and satisfies any requirement.
        """
        if not required_scopes:
            return True

        if not self.scopes:
            return True

        granted_scopes = set(self.scopes)
        return all(scope in granted_scopes for scope in required_scopes)

    def _has_expired(self) -> bool:
        from django.utils import timezone
        if self.expiry_date is None:
            return False
        return self.expiry_date < timezone.now()

    _has_expired.short_description = "Has expired"
    _has_expired.boolean = True
    has_expired = property(_has_expired)

    class Meta:
        abstract = True
        verbose_name = "API key"
        verbose_name_plural = "API keys"

    def __str__(self) -> str:
        return self.name or ""


class APIKey(AbstractAPIKey):
    """
    API KEY model
    """

    pass
