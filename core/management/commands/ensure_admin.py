import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the first superuser from environment variables when no user exists.'

    def handle(self, *args, **options):
        if os.environ.get('CREATE_DEFAULT_ADMIN', '1').strip().lower() not in {'1', 'true', 'yes', 'on'}:
            self.stdout.write('Default admin creation is disabled.')
            return

        username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin').strip()
        email = os.environ.get('DEFAULT_ADMIN_EMAIL', '').strip()
        password = os.environ.get('DEFAULT_ADMIN_PASSWORD', '').strip()

        if not password:
            self.stdout.write(self.style.WARNING('DEFAULT_ADMIN_PASSWORD is not set; skipping default admin creation.'))
            return

        User = get_user_model()
        if User.objects.exists():
            self.stdout.write('Users already exist; skipping default admin creation.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created default superuser: {username}'))
