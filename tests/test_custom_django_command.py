import pytest

from io import StringIO

from django.core.management import call_command


def test_command_generate_fernet_key():
    out = StringIO()
    args = []
    opts = {}

    call_command("generate_fernet_key", *args, **opts, stdout=out)

    message = out.getvalue()

    assert message is not None
    assert type(message) is str
