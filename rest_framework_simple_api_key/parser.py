from rest_framework_simple_api_key.settings import package_settings


class APIKeyParser:
    keyword = package_settings.AUTHENTICATION_KEYWORD_HEADER
    message = "No API KEY provided."

    def get(self):
        pass

    def get_from_authorization(self):
        pass

    def get_from_header(self):
        pass
