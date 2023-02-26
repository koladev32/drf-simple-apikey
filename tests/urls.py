from django.urls import path

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from rest_framework_simple_api_key.backends import APIKeyAuthentication
from rest_framework_simple_api_key.permissions import IsActiveEntity


@api_view()
@authentication_classes([APIKeyAuthentication])
@permission_classes([IsActiveEntity])
def view(request: Request) -> Response:
    return Response({"detail: success"}, status=200)


urlpatterns = [
    path("test-request/", view, name="test-request")
]
