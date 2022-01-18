"""
Any custom permissions for the tracking api
"""
from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        if view.kwargs.get('user_id'):
            return request.user.id == view.kwargs.get('user_id')

        return True

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user) or request.user.is_staff
