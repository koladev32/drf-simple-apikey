from __future__ import annotations

from django.core.cache import cache
from django.apps import apps
from django.utils import timezone

from drf_simple_apikey.settings import package_settings

ROTATION_STATUS_CACHE_KEY = "rotation_status"

# How long a "no active rotation" result stays cached. This is deliberately
# short and bounded (unlike the "rotation is active" case, which is cached
# for the full ROTATION_PERIOD): it's a self-healing safety net in case some
# code path starts or stops a Rotation without calling
# invalidate_rotation_status_cache() below, so the package doesn't get stuck
# believing rotation is disabled indefinitely.
_NEGATIVE_CACHE_TIMEOUT = 60


def invalidate_rotation_status_cache() -> None:
    """
    Call this whenever a `Rotation` row is created, started, or stopped, so
    `get_rotation_status()` recomputes its value on the next call instead of
    returning a stale cached result.
    """
    cache.delete(ROTATION_STATUS_CACHE_KEY)


def get_rotation_status() -> bool:
    rotation_status = cache.get(ROTATION_STATUS_CACHE_KEY)

    if (
        rotation_status is None
    ):  # We should check for 'None' specifically because the cached value could be False
        # Lazy load the Rotation model
        Rotation = apps.get_model("drf_simple_apikey_rotation", "Rotation")

        # Filter the latest rotation that is enabled
        config = (
            Rotation.objects.filter(is_rotation_enabled=True)
            .order_by("-started")
            .first()
        )

        # If we have a rotation config and its 'ended' date has passed, update it
        if config and config.ended and config.ended <= timezone.now():
            config.is_rotation_enabled = False
            config.save()
            rotation_status = False
        elif config:
            rotation_status = True
        else:
            rotation_status = False

        # Cache the rotation status
        cache.set(
            ROTATION_STATUS_CACHE_KEY,
            rotation_status,
            (
                package_settings.ROTATION_PERIOD.total_seconds()
                if rotation_status
                else _NEGATIVE_CACHE_TIMEOUT
            ),
        )  # Cache for the rotation period if true, briefly otherwise

    return rotation_status
