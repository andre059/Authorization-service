from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Пользователь"""

    email = models.EmailField(unique=True, verbose_name='почта')
    phone_number = models.CharField(max_length=15, unique=True, default='', verbose_name='номер телефона')
    country = models.CharField(max_length=100, **NULLABLE, verbose_name='страна')
    city = models.CharField(max_length=150, **NULLABLE, verbose_name='город')
    is_active = models.BooleanField(default=False, verbose_name='активный')
    date_of_birth = models.DateField(**NULLABLE, verbose_name='дата рождения')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    authorization_code = models.CharField(max_length=4, **NULLABLE, verbose_name='кода авторизации')
    referral_code = models.CharField(max_length=6,
                                     default=''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
                                     verbose_name='инвайт-код')
    referred_by = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, related_name='referrals',
                                    verbose_name='кто пригласил текущего пользователя')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
