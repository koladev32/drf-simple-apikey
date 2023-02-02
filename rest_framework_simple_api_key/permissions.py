import typing

from django.http import HttpRequest
from rest_framework.permissions import BasePermission


class IsActiveEntity(BasePermission):
    message = "Entity is not active."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:

        print(request.user)

        return request.user.is_active

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj
    ) -> bool:

        return request.user.is_active
