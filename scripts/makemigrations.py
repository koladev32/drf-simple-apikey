"""A stand-alone equivalent of `python manage.py makemigrations`."""
import pathlib
import sys

import django
from django.core.management import call_command

root = pathlib.Path(__file__).parent.parent
sys.path.append(str(root))

if __name__ == "__main__":

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
            "rest_framework_simple_api_key.rotation",
            "rest_framework_simple_api_key.analytics",
            "tests",
        ),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        SIMPLE_API_KEY={
            "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA=",
        },
    )

    django.setup()

    # For available options, see:
    # https://docs.djangoproject.com/en/3.0/ref/django-admin/#makemigrations
    if len(sys.argv) > 1:
        app_labels = sys.argv[1:]
        call_command("makemigrations", *app_labels)
    else:
        print(
            "No app label provided. Usage: python -m scripts.makemigrations [app_label]"
        )
