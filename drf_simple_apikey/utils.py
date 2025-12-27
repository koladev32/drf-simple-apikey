from __future__ import annotations

import typing

from django.http import HttpRequest

from drf_simple_apikey.parser import APIKeyParser


def get_key(key_parser: APIKeyParser, request: HttpRequest) -> str | None:
    return key_parser.get(request)
