from django.contrib import admin
from .models import WhitelistedIP, BlacklistedIP


@admin.register(WhitelistedIP)
class WhitelistedIPAdmin(admin.ModelAdmin):
    """
    Admin configuration for the WhitelistedIP model.

    Displays the IP address, description, and added date in the Django Admin.
    """
    list_display = ('ip_address', 'description', 'added_on')
    search_fields = ('ip_address', 'description')


@admin.register(BlacklistedIP)
class BlacklistedIPAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BlacklistedIP model.

    Displays the IP address, reason, and added date in the Django Admin.
    """
    list_display = ('ip_address', 'reason', 'added_on')
    search_fields = ('ip_address', 'reason')
