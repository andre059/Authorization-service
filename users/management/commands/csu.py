import os

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('EMAIL_HOST_USER'),
            first_name='Admin',
            last_name='Adminich',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password.os.getenv('CSU_SET_PASSWORD')
        user.save()
