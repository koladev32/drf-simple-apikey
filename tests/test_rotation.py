import os

import pytest
from django.core.cache import cache
from django.core.management import call_command

from drf_simple_apikey.rotation.utils import (
    ROTATION_STATUS_CACHE_KEY,
    get_rotation_status,
)

pytestmark = pytest.mark.django_db

ROTATION_ENABLED = bool(os.environ.get("TEST_WITH_ROTATION"))


@pytest.mark.skipif(
    not ROTATION_ENABLED, reason="Requires the rotation app (TEST_WITH_ROTATION=1)"
)
class TestRotationStatusCache:
    def setup_method(self):
        from drf_simple_apikey.rotation.models import Rotation

        cache.delete(ROTATION_STATUS_CACHE_KEY)
        Rotation.objects.all().delete()

    def test_starting_rotation_via_command_invalidates_stale_cached_status(self):
        # Cache the "no rotation" result, exactly as authenticating a
        # request naturally would before any rotation is started.
        assert get_rotation_status() is False

        call_command("rotation")

        # Before the fix, this kept returning the stale cached False
        # forever, since the negative result was cached with timeout=None
        # and nothing invalidated it when the rotation started.
        assert get_rotation_status() is True

    def test_stopping_rotation_via_command_invalidates_stale_cached_status(self):
        call_command("rotation")
        assert get_rotation_status() is True

        call_command("rotation", "--stop")

        assert get_rotation_status() is False


@pytest.mark.skipif(
    not ROTATION_ENABLED, reason="Requires the rotation app (TEST_WITH_ROTATION=1)"
)
class TestRotationAdminCacheInvalidation:
    def setup_method(self):
        from drf_simple_apikey.rotation.models import Rotation

        cache.delete(ROTATION_STATUS_CACHE_KEY)
        Rotation.objects.all().delete()

    def test_creating_a_rotation_via_admin_invalidates_stale_cached_status(self, rf):
        from django.contrib.admin import site

        from drf_simple_apikey.rotation.admin import RotationAdmin
        from drf_simple_apikey.rotation.models import Rotation

        from .test_admin import build_admin_request

        assert get_rotation_status() is False

        request = build_admin_request(rf)
        admin = RotationAdmin(Rotation, site)
        rotation = Rotation(is_rotation_enabled=False)
        admin.save_model(request, obj=rotation)

        assert get_rotation_status() is True
