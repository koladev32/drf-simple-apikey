import typing

from django.http import HttpRequest
from rest_framework.permissions import BasePermission


class IsActiveEntity(BasePermission):
    """
    A base permission that only checks if the entity (by default, the Django user) is
    active or not.
    """

    message = "Entity is not active."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.user.is_active

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj
    ) -> bool:
        return request.user.is_active


class ReadOnlyEntity(BasePermission):

    message = "This resource is read only."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.method == "GET"

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj
    ) -> bool:
        return request.method == "GET"


class CreateOnlyEntity(BasePermission):

    message = "This resource is create only."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.method == "POST"

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj
    ) -> bool:
        return request.method == "POST"


class UpdateOnlyEntity(BasePermission):

    message = "This resource is update only."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.method == "PUT"

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj
    ) -> bool:
        return request.method == "PUT"

