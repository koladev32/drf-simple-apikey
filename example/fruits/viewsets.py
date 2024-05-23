from django.shortcuts import render

from rest_framework import viewsets

from drf_apikey.backends import APIKeyAuthentication
from drf_apikey.permissions import IsActiveEntity
from rest_framework.response import Response


class FruitViewSets(viewsets.ViewSet):
    http_method_names = ["get"]
    authentication_classes = (APIKeyAuthentication,)
    permission_classes = (IsActiveEntity,)

    def list(self, request):
        return Response([{"detail": True}], 200)
