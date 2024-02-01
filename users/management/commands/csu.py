import os

from django.core.management import BaseCommand
from users.models import User
from users.services import generate_temp_email

temp_email = generate_temp_email()


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number=os.getenv('PHONE_NUMBER_HOST_USER'),
            first_name='A',
            last_name='A',
            is_active=True,
            is_staff=True,
            is_superuser=True,
            is_authorized=True,
            is_authenticated=True,
            email=temp_email
        )

        password = os.getenv('CSU_SET_PASSWORD')
        user.set_password(password)
        user.save()
