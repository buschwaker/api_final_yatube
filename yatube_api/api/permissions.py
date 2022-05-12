from rest_framework import permissions
from rest_framework.exceptions import ParseError


class NotSelfSubscription(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
                request.method in permissions.SAFE_METHODS or
                request.data.get('following') != request.user.username
        ):
            return True
        else:
            raise ParseError("Пользователь не может подписаться на себя!")
