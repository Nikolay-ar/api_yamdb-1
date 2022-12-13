from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка прав админа"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )

    def has_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )


class IsUserOrIsModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Кастомный класс прав на просмотр от всех пользователей"""
    def has_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or obj.author == request.user
            or request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or obj.author == request.user
            or request.user.is_moderator
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Кастомный класс прав на просмотр от Админа"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )

    def has_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )
