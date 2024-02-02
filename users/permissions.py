from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken


class UserIsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:  # проверка на менеджера
            return True
        else:
            return False


class IsVerifiedUser(BasePermission):
    """Проверяет, есть ли у пользователя разрешение на доступ к запрашиваемому представлению."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:  # Проверяем, не является ли пользователь анонимным
            return False
        elif request.user.is_authorized:
            return True
        raise PermissionDenied("Пользователь не авторизован или не прошел проверку верификации")


class IsOwnerOrReadOnly(BasePermission):
    """ Проверяет, является ли пользователь владельцем профиля """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
