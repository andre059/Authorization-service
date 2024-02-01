from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'first_name', 'last_name', 'country', 'city', 'is_active',
                  'date_of_birth', 'avatar', 'referral_code', 'referred_by', 'is_authorized', 'is_authenticated']


class PhoneNumberAndCodeTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')

        if not phone_number:
            raise serializers.ValidationError("No phone number provided")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError('Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.')
        return value

    def validate(self, data):
        if not all(data.values()):
            raise serializers.ValidationError("Заполните все обязательные поля.")

        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError("Новые пароли не совпадают.")

        return data
