from rest_framework.permissions import BasePermission
from django.http import HttpRequest
from .models import WhitelistedIP, BlacklistedIP
from drf_simple_apikey.settings import package_settings

class IPWhitelistBlacklistPermission(BasePermission):
    """
    Permission class to restrict access based on IP whitelisting and blacklisting.

    - Grants access if the request's IP is in the WhitelistedIP model.
    - Denies access if the request's IP is in the BlacklistedIP model.
    - If there are no entries in the whitelist, defaults to open access unless blacklisted.

    Attributes:
        message (str): Message returned when access is denied.
    """

    message = "Access denied due to IP restrictions."

    def has_permission(self, request: HttpRequest, view: object) -> bool:
        """
        Checks if the client's IP is whitelisted or blacklisted.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (object): The view being accessed.

        Returns:
            bool: True if the IP is whitelisted or if no whitelist is defined; False if blacklisted.
        """
        client_ip = request.META.get(package_settings.IP_ADDRESS_HEADER, '')

        # Deny access if IP is in the blacklist
        if BlacklistedIP.objects.filter(ip_address=client_ip).exists():
            return False

        # Allow access if IP is in the whitelist; if no whitelist, allow all by default
        if WhitelistedIP.objects.exists():
            return WhitelistedIP.objects.filter(ip_address=client_ip).exists()

        return True
