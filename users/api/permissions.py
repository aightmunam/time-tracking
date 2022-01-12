"""
Any custom permissions for the users api
"""
from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only allow a user that is the owner of the instance or
    an admin user to access
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.user.is_authenticated and request.user.username == obj.username:
            return True

        return False
