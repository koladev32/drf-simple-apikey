import croniter
from django.utils.timezone import now, datetime
from rest_framework_simple_api_key.settings import package_settings


def rotation_happening() -> bool:
    
    cron_date = croniter(package_settings.ROTATION_DATE, now())

    rotation_datetime = cron_date.get_prev(datetime)

    return (
        package_settings.ROTATION_ENABLED
        or rotation_datetime
        <= now()
        <= rotation_datetime + package_settings.ROTATION_PERIOD
    ) # FIXME: should not return True if a rotation has never happened yet. It means that the
    # package is freshly installed.
