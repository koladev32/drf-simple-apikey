# Your app's management/commands/handle_rotation.py

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from drf_simple_apikey.rotation.models import Rotation
from drf_simple_apikey.settings import package_settings


class Command(BaseCommand):
    help = "Starts or stops a rotation based on command arguments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--stop",
            action="store_true",
            help="Stops the rotation (Default is to start)",
        )

    def handle(self, *args, **options):
        if options["stop"]:
            # Stop the rotation logic
            try:
                rotation = Rotation.objects.filter(is_rotation_enabled=True).latest(
                    "started"
                )
                rotation.is_rotation_enabled = False
                rotation.ended = timezone.now()
                rotation.save()
                self.stdout.write(self.style.SUCCESS("Successfully stopped rotation"))
            except Rotation.DoesNotExist:
                raise CommandError("No active rotation found to stop")
        else:
            # Start the rotation logic
            obj = Rotation()
            obj.is_rotation_enabled = True
            obj.ended = timezone.now() + package_settings.ROTATION_PERIOD
            obj.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully started rotation ending at {obj.ended}"
                )
            )
