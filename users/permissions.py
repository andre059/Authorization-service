from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from users.models import User


class UserIsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:  # проверка на менеджера
            return True
        else:
            return False


class IsVerifiedUser(BasePermission):
    """
    Проверяет, есть ли у пользователя разрешение на доступ к запрашиваемому представлению.
    """
    def has_permission(self, request, view):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if user.is_authorized:
            return True
        raise PermissionDenied("Пользователь не авторизован или не прошел проверку верификации")