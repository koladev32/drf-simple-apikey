import typing

from django.contrib import admin, messages
from django.http.request import HttpRequest

from .models import APIKey


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = (
        "entity",
        "revoked",
        "expiry_date",
        "created",
    )

    list_filter = (
        "entity",
        "revoked",
        "expiry_date",
        "created",
    )

    def get_readonly_fields(
        self, request: HttpRequest, obj: APIKey = None
    ) -> typing.Tuple[str, ...]:
        fields = (
            "entity",
            "created",
        )

        if obj and obj.revoked:
            fields += (
                "name",
                "revoked",
                "expiry_date",
            )

        return fields

    def save_model(
        self,
        request: HttpRequest,
        obj: APIKey,
        form: typing.Any = None,
        change: bool = False,
    ) -> None:
        """
        If there is obj.pk, it means that the object is being created. We need then to display the
        `api_key` value in the Django admin dashboard.
        """

        if not obj.pk:
            obj.save()

            key = self.model.objects.assign_api_key(obj)

            message = (
                "The API key is: {}. ".format(key)
                + "Please store it somewhere safe: "
                + "you will not be able to see it again."
            )
            messages.add_message(request, messages.WARNING, message)
        else:
            obj.save()


admin.site.register(APIKey, ApiKeyAdmin)
