"""A stand-alone equivalent of `python manage.py makemigrations`."""
import pathlib
import sys

import django
from django.core.management import call_command

root = pathlib.Path(__file__).parent.parent
sys.path.append(str(root))

if __name__ == "__main__":
    APP = "rest_framework_simple_api_key"

    from django.conf import settings

    settings.configure(
        SECRET_KEY="foo",
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "rest_framework",
            "rest_framework_simple_api_key",
            "tests",
        ),
        SIMPLE_API_KEY={
            "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA=",
        },
    )

    django.setup()

    # For available options, see:
    # https://docs.djangoproject.com/en/3.0/ref/django-admin/#makemigrations
    options = sys.argv[1:]
    call_command("makemigrations", *options, APP)
