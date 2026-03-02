# from rest_framework.permissions import BasePermission

# class IsAdminRole(BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated and
#             (
#                 request.user.role == "admin"
#                 or request.user.is_staff
#                 or request.user.is_superuser
#             )
#         )
from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        # ✅ Conserve la logique admin existante ET ajoute establishment
        return (
            request.user.is_authenticated and
            (
                request.user.role in ["admin", "etablissement"]
                or request.user.is_staff
                or request.user.is_superuser
            )
        )