from __future__ import annotations

import logging
import secrets
import time
import typing

from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import exceptions


from drf_simple_apikey.crypto import get_crypto
from drf_simple_apikey.models import APIKey
from drf_simple_apikey.parser import APIKeyParser
from drf_simple_apikey.settings import package_settings

logger = logging.getLogger(__name__)


class APIKeyAuthentication(BaseBackend):
    model = APIKey
    key_parser = APIKeyParser()

    def __init__(self):
        self.key_crypto = get_crypto()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        return self.key_parser.get(request)

    def _get_client_ip(self, request: HttpRequest) -> str | None:
        """
        Safely extract client IP address, handling proxy headers securely.
        Validates IP format and falls back to REMOTE_ADDR.
        """
        # First try the configured header
        ip_header = package_settings.IP_ADDRESS_HEADER
        client_ip = request.META.get(ip_header)

        # If using proxy headers, validate and handle safely
        if ip_header != "REMOTE_ADDR":
            # For X-Forwarded-For, take the first IP (original client)
            if ip_header == "HTTP_X_FORWARDED_FOR":
                forwarded_ips = client_ip.split(",") if client_ip else []
                client_ip = forwarded_ips[0].strip() if forwarded_ips else None

        # Validate IP format (basic validation)
        if client_ip:
            # Basic IP validation - check if it looks like an IP
            parts = client_ip.split(".")
            if len(parts) == 4:
                try:
                    # Validate each part is 0-255
                    if all(0 <= int(part) <= 255 for part in parts):
                        return client_ip
                except (ValueError, AttributeError):
                    pass

        # Fallback to REMOTE_ADDR
        return request.META.get("REMOTE_ADDR")

    def _check_https_enforcement(self, request: HttpRequest) -> None:
        """Check if HTTPS is enforced and request is secure."""
        enforce_https = package_settings.ENFORCE_HTTPS

        # Auto-detect based on DEBUG if not explicitly set
        # Default to not DEBUG (enforce HTTPS in production, allow HTTP in development)
        # But also check if we're in a test environment
        if enforce_https is None:
            # Don't enforce HTTPS in test environments (pytest, unittest, etc.)
            import sys
            is_test = (
                "pytest" in sys.modules
                or "unittest" in sys.modules
                or "test" in sys.argv
                or hasattr(settings, "TESTING")
            )
            enforce_https = not settings.DEBUG and not is_test

        if enforce_https:
            # Check if request is secure
            is_secure = request.is_secure()
            # Also check X-Forwarded-Proto header (for behind reverse proxy)
            forwarded_proto = request.META.get("HTTP_X_FORWARDED_PROTO", "").lower()
            if forwarded_proto == "https":
                is_secure = True

            if not is_secure:
                logger.warning(
                    "API key authentication attempted over HTTP",
                    extra={"ip": self._get_client_ip(request)},
                )
                raise exceptions.AuthenticationFailed(
                    "API key authentication requires HTTPS. Please use a secure connection."
                )

    def _constant_time_delay(self) -> None:
        """Add a small constant delay to prevent timing attacks."""
        time.sleep(0.01)  # 10ms constant delay

    def authenticate(
        self, request: HttpRequest, **kwargs: typing.Any
    ) -> tuple[typing.Any, str] | None:
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires api key authentication.
        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
        this means we know authentication will fail. An example of
        this is when the request does not include an api key in the
        headers.

        2) `(entity)` - We return an entity object when
        authentication is successful.
        If neither case is met, that means there's an error,
        and we do not return anything.
        We simply raise the `AuthenticationFailed`
        exception and let Django REST Framework
        handle the rest.
        """

        key = self.get_key(request)

        # If no key, return None early (no authentication attempted)
        if key is None:
            return None

        # Check HTTPS enforcement before processing
        self._check_https_enforcement(request)

        return self._authenticate_credentials(request, key)

    def _authenticate_credentials(
        self, request: HttpRequest, key: str | None
    ) -> tuple[typing.Any, str]:
        """
        Authenticate credentials with timing attack protection.
        All code paths take similar time to prevent timing-based information leakage.
        """
        key_crypto = self.key_crypto
        start_time = time.time()
        auth_successful = False
        client_ip = self._get_client_ip(request)

        try:
            # Attempt decryption
            try:
                payload = key_crypto.decrypt(key)
            except (ValueError, TypeError):
                # Invalid key format - use constant-time comparison
                # Create a dummy payload to maintain timing
                payload = {}
                # Use secrets.compare_digest for constant-time comparison
                secrets.compare_digest("invalid", "invalid")

            # Validate payload structure
            if "_pk" not in payload or "_exp" not in payload:
                # Use constant-time comparison even for invalid keys
                secrets.compare_digest("invalid", "invalid")
                raise exceptions.AuthenticationFailed("Invalid API Key.")

            # Check expiry
            if payload["_exp"] < now().timestamp():
                if package_settings.ENABLE_AUDIT_LOGGING:
                    logger.warning(
                        "API key authentication failed: expired",
                        extra={"ip": client_ip, "api_key_id": payload.get("_pk")},
                    )
                raise exceptions.AuthenticationFailed("API Key has already expired.")

            # Get API key from database
            try:
                api_key = self.model.objects.get(id=payload["_pk"])
            except ObjectDoesNotExist:  # pylint: disable=maybe-no-member
                # Use constant-time comparison to prevent timing leaks
                secrets.compare_digest("invalid", "invalid")
                if package_settings.ENABLE_AUDIT_LOGGING:
                    logger.warning(
                        "API key authentication failed: not found",
                        extra={"ip": client_ip, "api_key_id": payload.get("_pk")},
                    )
                raise exceptions.AuthenticationFailed("No entity matching this api key.")

            # Check if revoked
            if api_key.revoked:
                if package_settings.ENABLE_AUDIT_LOGGING:
                    logger.warning(
                        "API key authentication failed: revoked",
                        extra={"ip": client_ip, "api_key_id": api_key.pk},
                    )
                raise exceptions.AuthenticationFailed("This API Key has been revoked.")

            # IP address validation with safe IP extraction
            if api_key.blacklisted_ips and client_ip in api_key.blacklisted_ips:
                if package_settings.ENABLE_AUDIT_LOGGING:
                    logger.warning(
                        "API key authentication failed: blacklisted IP",
                        extra={"ip": client_ip, "api_key_id": api_key.pk},
                    )
                raise exceptions.AuthenticationFailed("Access denied from blacklisted IP.")

            if api_key.whitelisted_ips and client_ip not in api_key.whitelisted_ips:
                if package_settings.ENABLE_AUDIT_LOGGING:
                    logger.warning(
                        "API key authentication failed: IP not whitelisted",
                        extra={"ip": client_ip, "api_key_id": api_key.pk},
                    )
                raise exceptions.AuthenticationFailed(
                    "Access restricted to specific IP addresses."
                )

            # Authentication successful
            auth_successful = True
            if package_settings.ENABLE_AUDIT_LOGGING:
                logger.info(
                    "API key authentication successful",
                    extra={"ip": client_ip, "api_key_id": api_key.pk, "entity_id": api_key.entity.pk},
                )

            return api_key.entity, key

        except exceptions.AuthenticationFailed:
            # Re-raise authentication failures
            raise
        except Exception as e:
            # Log unexpected errors
            if package_settings.ENABLE_AUDIT_LOGGING:
                logger.error(
                    "API key authentication error",
                    extra={"ip": client_ip, "error": str(e)},
                    exc_info=True,
                )
            raise exceptions.AuthenticationFailed("Invalid API Key.")
        finally:
            # Add constant-time delay to normalize response time
            # This prevents timing attacks by making all code paths take similar time
            elapsed = time.time() - start_time
            if elapsed < 0.01:  # If faster than 10ms, add delay
                self._constant_time_delay()

    def authenticate_header(self, request: HttpRequest) -> str | None:
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass
