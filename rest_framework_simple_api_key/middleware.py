from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from rest_framework_simple_api_key.backends import APIKeyAuthentication


class ApiKeyAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        api_key_authentication = APIKeyAuthentication()
        entity, _ = api_key_authentication.authenticate(request)
        custom_entity_name = settings.SIMPLE_API_KEY["custom_entity_name"]

        if not hasattr(request, custom_entity_name):
            setattr(request, custom_entity_name, entity)
