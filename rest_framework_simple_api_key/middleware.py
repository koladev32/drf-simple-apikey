from django.conf import settings
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


class ApiKeyAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django Rest Framework Simple API Key authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'rest_framework_simple_api_key.middleware.ApiKeyAuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        custom_entity_name = settings.SIMPLE_API_KEY["custom_entity_name"]
        setattr(request, custom_entity_name, SimpleLazyObject(lambda: get_user(request)))
