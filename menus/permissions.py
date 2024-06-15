from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class IsOwnerOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        # Allow access if the user is a superuser
        if request.user and request.user.is_superuser:
            return True

        # Allow access if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is a superuser
        if request.user and request.user.is_superuser:
            return True

        # Allow access if the user is the owner of the menu
        if hasattr(obj, "menu") and obj.menu.owner == request.user:
            return True

        # Allow access if the user is the owner of the category's menu
        if hasattr(obj, "category") and obj.category.menu.owner == request.user:
            return True

        # Deny access otherwise
        raise PermissionDenied(_("You do not have permission to perform this action."))
