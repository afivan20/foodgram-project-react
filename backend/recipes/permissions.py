from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAuthenticatedAndOwner(BasePermission):
    """
    Allows access to authenticated users, and owners.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if (request.method == 'DELETE' or request.method == 'PATCH' or request.method == 'PUT'):
            return obj.author == request.user
        else:
            return True
