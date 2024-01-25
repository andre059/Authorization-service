from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'country', 'city', 'is_active', 'date_of_birth', 'avatar',
                  'authorization_code', 'referral_code', 'referred_by', 'is_authorized']
        permission_classes = [IsAuthenticated]

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Добавление пользовательских полей в токен
#         token['username'] = user.username
#         token['email'] = user.email
#
#         return token
