from django.core.cache import cache
from django.apps import apps

from rest_framework_simple_api_key.settings import package_settings


def get_rotation_status():
    rotation_status = cache.get("rotation_status")

    if not rotation_status:
        # Lazy load the RotationConfig model
        RotationConfig = apps.get_model('rest_framework_simple_api_key_rotation', 'RotationConfig')

        config = RotationConfig.objects.last()
        rotation_status = config.is_rotation_enabled if config else False
        cache.set(
            "rotation_status",
            rotation_status,
            package_settings.ROTATION_PERIOD.total_seconds(),
        )  # Cache for the rotation period

    return rotation_status
