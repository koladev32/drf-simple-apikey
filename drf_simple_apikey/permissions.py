from __future__ import annotations

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
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return request.user.is_active


class ReadOnlyEntity(BasePermission):

    message = "This resource is read only."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.method == "GET"

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return request.method == "GET"


class CreateOnlyEntity(BasePermission):

    message = "This resource is create only."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.method == "POST"

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return request.method == "POST"


class UpdateOnlyEntity(BasePermission):

    message = "This resource is update only."

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return request.method == "PUT"

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return request.method == "PUT"


class HasAPIKeyScopes(BasePermission):
    """
    A permission that checks the API key used to authenticate the request
    carries all the scopes required by the view.

    Required scopes are declared on the view with a `required_scopes`
    attribute, e.g. `required_scopes = ["fruits:read"]`. A key with no
    scopes configured is unrestricted and satisfies any requirement.
    """

    message = "This API key does not have the required scope(s) for this action."

    def _has_required_scopes(self, request: HttpRequest, view: typing.Any) -> bool:
        required_scopes = getattr(view, "required_scopes", None) or []
        api_key = getattr(request, "auth", None)

        if not required_scopes:
            return True

        if api_key is None or not hasattr(api_key, "has_scopes"):
            return False

        return api_key.has_scopes(required_scopes)

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        return self._has_required_scopes(request, view)

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return self._has_required_scopes(request, view)
