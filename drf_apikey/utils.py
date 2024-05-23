import typing

from django.http import HttpRequest


def get_key(key_parser, request: HttpRequest) -> typing.Optional[str]:
    return key_parser.get(request)
