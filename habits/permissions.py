from rest_framework.permissions import BasePermission


class IsOwnerOrPublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.is_public
