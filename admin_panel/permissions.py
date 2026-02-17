from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Autorise uniquement les utilisateurs ayant role='admin'
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "admin"
        )
