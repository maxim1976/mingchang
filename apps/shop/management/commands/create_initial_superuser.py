import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates an initial superuser if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists. Skipping creation.'))
            return

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@mingchang.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme123')

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser: {username}')
            )
            self.stdout.write(
                self.style.WARNING(f'Default password: {password}')
            )
            self.stdout.write(
                self.style.WARNING('IMPORTANT: Change the password immediately after first login!')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
