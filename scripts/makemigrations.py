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

    MIDDLEWARE = (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    )

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        SITE_ID=1,
        SECRET_KEY="nothing to hide in tests",
        USE_I18N=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        MIDDLEWARE=MIDDLEWARE,
        MIDDLEWARE_CLASSES=MIDDLEWARE,
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
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        SIMPLE_API_KEY={
            "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA=",
            "API_KEY_LIFETIME": 365,
            "AUTHENTICATION_MODEL": "auth.User",
        },
    )

    django.setup()

    # For available options, see:
    # https://docs.djangoproject.com/en/3.0/ref/django-admin/#makemigrations
    options = sys.argv[1:]
    call_command("makemigrations", *options, APP)
