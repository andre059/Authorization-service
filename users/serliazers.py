from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'country', 'city', 'is_active', 'date_of_birth', 'avatar',
                  'authorization_code', 'referral_code', 'referred_by', 'is_authorized']


class PhoneNumberAndCodeTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(required=True)
    authorization_code = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        authorization_code = attrs.get('authorization_code')

        if not phone_number or not authorization_code:
            raise serializers.ValidationError("No phone number or authorization code provided")

        try:
            user = User.objects.get(phone_number=phone_number, authorization_code=authorization_code)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number or authorization code")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
