from django.core.cache import cache
from django.apps import apps
from django.utils import timezone

from rest_framework_simple_api_key.settings import package_settings


def get_rotation_status():
    rotation_status = cache.get("rotation_status")

    if (
        rotation_status is None
    ):  # We should check for 'None' specifically because the cached value could be False
        # Lazy load the Rotation model
        Rotation = apps.get_model("rest_framework_simple_api_key_rotation", "Rotation")

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
            "rotation_status",
            rotation_status,
            package_settings.ROTATION_PERIOD.total_seconds()
            if rotation_status
            else None,
        )  # Cache for the rotation period if true

    return rotation_status
