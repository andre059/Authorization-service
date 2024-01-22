import random
import time

from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serliazers import UserSerializers
from users.services import generate_authorization_code


class UserViewSet(viewsets.ModelViewSet):
    """класс для вывода списка и информации по одному объекту"""

    serializer_class = UserSerializers
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]


class PhoneAuthorizationView(APIView):
    """Авторизация по телефону"""

    def post(self, request, format='json'):
        """обработка запроса на ввод номера телефона и отправки кода аутентификации"""

        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Требуется номер телефона'}, status=status.HTTP_400_BAD_REQUEST)

        # Имитация отправки 4-значного кода аутентификации с задержкой в 1-2 секунды
        authorization_code = random.randint(1000, 9999)
        time.sleep(random.uniform(1, 2))

        cache.set(phone_number, str(authorization_code), timeout=120)  # Сохранение кода в кэше

        print(authorization_code)
        return Response({'success': 'Номер телефона подтвержден. Отправлен код аутентификации.'},
                        status=status.HTTP_200_OK)

    def put(self, request, format='json'):
        """обработка запроса на ввод кода аутентификации"""

        phone_number = request.data.get('phone_number')
        authorization_code = request.data.get('authorization_code')

        if not phone_number or not authorization_code:
            return Response({'error': 'Требуется номер телефона и код'}, status=status.HTTP_400_BAD_REQUEST)

        stored_code = cache.get(phone_number)
        print("Сгенерированный код для номера телефона {}: {}".format(phone_number, stored_code))

        if stored_code and stored_code == authorization_code:
            # Действительный код, перейдите к аутентификации
            print(stored_code, authorization_code)
            return Response({'success': 'Номер телефона подтвержден. Пользователь прошел аутентификацию.'},
                            status=status.HTTP_200_OK)
        else:
            print(stored_code, authorization_code)
            return Response({'error': 'Недействительный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)


# class RequestAuthorizationCode(APIView):
#     """Обрабатывает запрос на получение кода авторизации."""
#
#     def post(self, request):
#         """
#         Обрабатывает POST-запрос, генерирует и отправляет код авторизации.
#         Args:
#         - request: Входной объект запроса.
#         Returns:
#         - Response: Ответ с данными о статусе операции.
#         """
#
#         phone_number = request.data.get('phone_number')
#
#         if phone_number:
#             user, created = User.objects.get_or_create(phone_number=phone_number)
#
#             if created or not user.authorization_code:
#                 user.authorization_code = generate_authorization_code()
#                 user.save()
#                 # Отправка кода, через сторонний сервис для отправки SMS
#                 return Response({'detail': 'Код авторизации был отправлен на номер телефона'},
#                                 status=status.HTTP_200_OK)
#         else:
#             return Response({'detail': 'Не указан номер телефона'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """Предоставляет детали профиля пользователя."""

    def get(self, request):
        """
        Обрабатывает GET-запрос для получения деталей профиля пользователя.

        Args:
        - request: Входной объект запроса.

        Returns:
        - Response: Ответ с деталями профиля пользователя.
        """

        user = request.user
        data = {
            'phone_number': user.phone_number,
            'country': user.country,
            'city': user.city,
            'date_of_birth': user.date_of_birth,
            'avatar': user.avatar.url if user.avatar else None,
            'referral_code': user.referral_code
        }
        return Response(data, status=status.HTTP_200_OK)


class CheckReferralCode(APIView):
    """Обрабатывает проверку инвайт-кода."""

    def post(self, request):
        """
        Обрабатывает POST-запрос для проверки и подтверждения инвайт-кода.

        Args:
        - request: Входной объект запроса.

        Returns:
        - Response: Ответ с данными о статусе проверки.
        """

        referral_code = request.data.get('referral_code')
        user = request.user
        try:
            referred_by = User.objects.get(referral_code=referral_code)
            if referred_by:
                user.referred_by = referred_by
                user.save()
                return Response({'detail': 'Инвайт-код подтвержден'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Неверный инвайт-код'}, status=status.HTTP_400_BAD_REQUEST)


class UsersReferredByCurrentUser(APIView):
    """Получает список пользователей, приглашенных текущим пользователем."""

    def get(self, request):
        """
        Обрабатывает GET-запрос для получения списка пользователей, приглашенных текущим пользователем.

        Args:
        - request: Входной объект запроса.

        Returns:
        - Response: Ответ со списком приглашенных пользователей.
        """

        user = request.user
        referred_users = User.objects.filter(referred_by=user)
        data = [{'username': user.username, 'id': user.id} for user in referred_users]
        return Response(data, status=status.HTTP_200_OK)
