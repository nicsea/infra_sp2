from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.is_admin


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin


class IsAuthorOrAdminOrModerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or obj.author == request.user
            or (request.user.is_authenticated
                and request.user.is_admin)
            or (request.user.is_authenticated
                and request.user.is_moderator)
        )
