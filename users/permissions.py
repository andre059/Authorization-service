from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


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
        if not request.user.is_authenticated:  # Проверяем, не является ли пользователь анонимным
            return False
        elif request.user.is_authorized:
            return True
        raise PermissionDenied("Пользователь не авторизован или не прошел проверку верификации")

