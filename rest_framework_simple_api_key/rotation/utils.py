from django.core.cache import cache

from rest_framework_simple_api_key.rotation.models import RotationConfig
from rest_framework_simple_api_key.settings import package_settings


def get_rotation_status():
    rotation_status = cache.get("rotation_status")

    if not rotation_status:
        config = RotationConfig.objects.first()
        rotation_status = config.is_rotation_enabled
        cache.set(
            "rotation_status",
            rotation_status,
            package_settings.ROTATION_PERIOD.total_seconds(),
        )  # Cache for the rotation period

    return rotation_status
