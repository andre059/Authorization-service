from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PhoneNumberBackend(ModelBackend):
    """Кастомный бэкэнд аутентификации"""

    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
