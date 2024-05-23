from cryptography.fernet import Fernet

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Displays the value of a Fernet key in the shell"

    def handle(self, *args, **options):
        key = Fernet.generate_key().decode()
        self.stdout.write(self.style.SUCCESS(key))
