from django.core.cache import cache

from rest_framework_simple_api_key.rotation.models import RotationConfig


def get_rotation_status():
    rotation_status = cache.get('rotation_status')

    if not rotation_status:
        config = RotationConfig.objects.first()
        rotation_status = config.is_rotation_enabled
        cache.set('rotation_status', rotation_status, 3600)  # Cache for 1 hour or as per your requirement

    return rotation_status
