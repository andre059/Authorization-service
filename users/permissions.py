from rest_framework.permissions import BasePermission


class UserIsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:  # проверка на менеджера
            return True
        else:
            return False