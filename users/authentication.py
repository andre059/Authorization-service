from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PhoneAndCodeBackend(ModelBackend):
    """Кастомный бэкэнд аутентификации"""

    def authenticate(self, request, phone_number=None, authorization_code=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=phone_number, authorization_code=authorization_code)
        except UserModel.DoesNotExist:
            return None
        else:
                return user
