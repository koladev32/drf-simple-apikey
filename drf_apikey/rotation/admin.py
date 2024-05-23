import typing

from django.contrib import admin, messages
from django.http.request import HttpRequest
from django.utils import timezone

from .models import Rotation
from ..settings import package_settings


class RotationAdmin(admin.ModelAdmin):
    list_display = (
        "is_rotation_enabled",
        "started",
        "ended",
    )

    list_filter = (
        "is_rotation_enabled",
        "started",
        "ended",
    )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Rotation = None
    ) -> typing.Tuple[str, ...]:
        fields = (
            "started",
            "ended",
        )

        return fields

    def save_model(
        self,
        request: HttpRequest,
        obj: Rotation,
        form: typing.Any = None,
        change: bool = False,
    ) -> None:
        """
        If there is obj.pk, it means that the object has been created already.
        """

        if not obj.pk:
            obj.is_rotation_enabled = True
            obj.ended = timezone.now() + package_settings.ROTATION_PERIOD
            obj.save()

            message = "A rotation is enabled."
            messages.add_message(request, messages.WARNING, message)
        else:
            obj.save()


admin.site.register(Rotation, RotationAdmin)
