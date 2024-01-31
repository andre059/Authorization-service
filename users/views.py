import random
import uuid

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsVerifiedUser
from users.serliazers import UserSerializers, PhoneNumberAndCodeTokenObtainPairSerializer, ChangePasswordSerializer


class PhoneAuthorizationView(APIView):
    """Авторизация по телефону"""

    def post(self, request):
        """обработка запроса на ввод номера телефона и отправки кода аутентификации"""

        phone_number = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.authorization_code:  # Если есть код, значит это второй запрос
                return Response({"detail": "Введите код авторизации"}, status=status.HTTP_200_OK)
            else:  # Пользователь уже существует, но кода нет - отправляем новый код
                authorization_code = ''.join(random.choices('0123456789', k=4))
                user.authorization_code = authorization_code
                user.save()
                return Response({"detail": "Код авторизации отправлен", "phone_number": phone_number,
                                 "authorization_code": authorization_code}, status=status.HTTP_200_OK)
        except User.DoesNotExist:  # Пользователь новый
            temp_email = f"{phone_number}-{uuid.uuid4()}@temp.com"  # временная почта
            user = User(phone_number=phone_number, email=temp_email)
            authorization_code = ''.join(random.choices('0123456789', k=4))
            user.authorization_code = authorization_code
            user.save()
            return Response({"detail": "Код авторизации отправлен", "phone_number": phone_number,
                             "authorization_code": authorization_code, "temp_email": temp_email},
                            status=status.HTTP_200_OK)

    def put(self, request):
        """обработка запроса на ввод кода аутентификации"""

        phone_number = str(request.data.get('phone_number'))
        authorization_code = str(request.data.get('authorization_code'))

        if not phone_number or not authorization_code:
            return Response({'error': 'Требуется номер телефона и код'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number, authorization_code=authorization_code)
            if user.authorization_code == authorization_code:  # Проверяем соответствие кода
                # Действительный код, обозначение пользователя как авторизованного
                user.is_authorized = True
                user.is_authenticated = True
                user.set_password(authorization_code)  # сохраняем код в пароле
                user.authorization_code = None  # удаляем код
                user.save()
                return Response({'success': 'Пользователь авторизован'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Недействительный код'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Недействительный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberAndCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneNumberAndCodeTokenObtainPairSerializer


class RefreshTokenView(APIView):
    def post(self, request):
        old_token_key = request.data['old_token_key']
        try:
            old_token = Token.objects.get(key=old_token_key)
            new_token = Token.objects.create(user=old_token.user)
            return Response({'new_token': new_token.key})
        except Token.DoesNotExist:
            return Response({'error': 'Old token does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Смена пароля"""

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        if not all([old_password, new_password1, new_password2]):
            raise ValidationError("Заполните все необходимые поля.")

        if not check_password(old_password, user.password):
            raise ValidationError("Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.")

        if new_password1 != new_password2:
            raise ValidationError("Новые пароли не совпадают.")

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)  # Обновление хэша сессии

        return Response({"detail": "Пароль успешно изменен"})


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsVerifiedUser]

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk'] or self.request.user.is_superuser


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsVerifiedUser]

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk'] or self.request.user.is_superuser


class UserDestroyAPIView(UserPassesTestMixin, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsVerifiedUser]

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk'] or self.request.user.is_superuser


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
        data = [{'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'id': user.id} for
                user in referred_users]
        return Response(data, status=status.HTTP_200_OK)
