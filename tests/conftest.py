import os

import pytest


def pytest_configure():
    from django.conf import settings

    MIDDLEWARE = (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    )

    apps = [
        "django.contrib.auth",
        "django.contrib.admin",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework_simple_api_key",
        "tests",
    ]

    if os.environ.get("TEST_WITH_ROTATION"):
        apps.append("rest_framework_simple_api_key.rotation")

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
        INSTALLED_APPS=apps,
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        SIMPLE_API_KEY={
            "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA=",
            "ROTATION_FERNET_SECRET": "EqkeOOgvV8bt70vUJiVXloNycn5bt_z1VqyoAi9K6f4=",
        },
    )

    try:
        import django

        django.setup()
    except AttributeError:
        pass


@pytest.fixture(autouse=True)
def setup_rotation_config(db):
    from django.conf import settings

    """Ensure a RotationConfig object exists for tests."""
    if "rest_framework_simple_api_key.rotation" in settings.INSTALLED_APPS:
        from rest_framework_simple_api_key.rotation.models import Rotation

        Rotation.objects.create(is_rotation_enabled=True)
