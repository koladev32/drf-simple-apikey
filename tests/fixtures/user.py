import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user():
    user = User.objects.create_user(
        **{
            "username": "narutos",
            "email": "naruto@datebayo.konoha",
            "password": "12345",
        }
    )

    return user
