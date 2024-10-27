from django.db import models


class WhitelistedIP(models.Model):
    """
    Model representing an IP address that is allowed to access the API.

    Attributes:
        ip_address (str): The IP address to whitelist.
        description (str): Optional description of the whitelisted IP.
        added_on (datetime): Timestamp when the IP was added to the whitelist.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ip_address} - {self.description or 'No description'}"


class BlacklistedIP(models.Model):
    """
    Model representing an IP address that is denied access to the API.

    Attributes:
        ip_address (str): The IP address to blacklist.
        reason (str): Optional reason for blacklisting the IP.
        added_on (datetime): Timestamp when the IP was added to the blacklist.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ip_address} - {self.reason or 'No reason'}"
