
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.shortcuts import get_object_or_404
# from django.contrib.auth import authenticate, get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from paths.models import Path  # ✅ Import du bon modèle
# from .permissions import IsAdminRole

# User = get_user_model()

# # =============================
# # LOGIN ADMIN
# # =============================
# class AdminLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         if not email or not password:
#             return Response({"error": "Email et mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(request, username=email, password=password)
#         if user is None:
#             return Response({"error": "Identifiants incorrects."}, status=status.HTTP_401_UNAUTHORIZED)

#         if not user.is_staff or str(getattr(user, "role", "")).lower() != "admin":
#             return Response({"error": "Accès réservé aux administrateurs."}, status=status.HTTP_403_FORBIDDEN)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "email": user.email,
#                 "username": user.username,
#                 "is_staff": user.is_staff,
#                 "role": getattr(user, "role", "participant"),
#             }
#         }, status=status.HTTP_200_OK)


# # =============================
# # SETUP ADMIN (temporaire)
# # =============================
# class SetupAdminView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         secret = request.query_params.get("secret")
#         if secret != "tektal2026":
#             return Response({"error": "Non autorisé"}, status=403)

#         user, created = User.objects.get_or_create(
#             email="admintest@tektal.com",
#             defaults={"username": "admin"}
#         )
#         user.username = "admin"
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.role = "admin"
#         user.set_password("Admin123456")
#         user.save()

#         return Response({
#             "message": "Admin créé" if created else "Admin mis à jour",
#             "role": user.role,
#             "is_staff": user.is_staff,
#         })


# # =============================
# # PATHS ADMIN (utilise le modèle de l'app paths)
# # =============================
# class PathListView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def get(self, request):
#         paths = Path.objects.all()
#         data = []
#         for path in paths:
#             steps_data = [
#                 {
#                     "step_number": s.step_number,
#                     "text": s.text,
#                     "start_time": s.start_time,
#                     "end_time": s.end_time,
#                 }
#                 for s in path.steps.all()
#             ]
#             data.append({
#                 "id": path.id,
#                 "title": path.title,
#                 "status": path.status,
#                 "author": path.author.username,
#                 "video_url": path.video_url,
#                 "duration": path.duration,
#                 "is_official": path.is_official,
#                 "start_label": path.start_label,
#                 "end_label": path.end_label,
#                 "created_at": path.created_at,
#                 "steps": steps_data,
#             })
#         return Response(data)


# class PathDetailView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def get(self, request, pk):
#         path = get_object_or_404(Path, pk=pk)
#         steps_data = [
#             {
#                 "step_number": s.step_number,
#                 "text": s.text,
#                 "start_time": s.start_time,
#                 "end_time": s.end_time,
#             }
#             for s in path.steps.all()
#         ]
#         return Response({
#             "id": path.id,
#             "title": path.title,
#             "status": path.status,
#             "author": path.author.username,
#             "video_url": path.video_url,
#             "duration": path.duration,
#             "is_official": path.is_official,
#             "start_label": path.start_label,
#             "end_label": path.end_label,
#             "created_at": path.created_at,
#             "steps": steps_data,
#         })


# class PathApproveView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def post(self, request, pk):
#         path = get_object_or_404(Path, pk=pk)
#         path.status = "APPROVED"
#         path.save()
#         return Response({"status": "approved"})


# class PathRejectView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def post(self, request, pk):
#         path = get_object_or_404(Path, pk=pk)
#         path.status = "REJECTED"
#         path.save()
#         return Response({"status": "rejected"})


# # =============================
# # PATHS PUBLICS
# # =============================
# class PublicPathListAPI(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         paths = Path.objects.filter(status="APPROVED")
#         data = [
#             {
#                 "id": p.id,
#                 "title": p.title,
#                 "video_url": p.video_url,
#                 "duration": p.duration,
#                 "is_official": p.is_official,
#                 "start_label": p.start_label,
#                 "end_label": p.end_label,
#                 "author": p.author.username,
#             }
#             for p in paths
#         ]
#         return Response(data)


# # =============================
# # UTILISATEURS
# # =============================
# class ConnectedUsersView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def get(self, request):
#         users = User.objects.filter(is_active=True)
#         data = [
#             {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "role": getattr(user, "role", "user"),
#             }
#             for user in users
#         ]
#         return Response(data)


# class UserDeleteView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def delete(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         if user.is_superuser:
#             return Response({"error": "Impossible de supprimer un superadmin."}, status=status.HTTP_403_FORBIDDEN)
#         user.delete()
#         return Response({"status": "deleted"})


# class UserToggleAdminView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminRole]

#     def post(self, request, pk):
#         user = get_object_or_404(User, pk=pk)

#         if user.is_superuser:
#             return Response({"role": user.role, "message": "Impossible de modifier le superadmin."}, status=status.HTTP_403_FORBIDDEN)

#         if user.role == "admin":
#             user.role = "participant"
#             user.is_staff = False
#         else:
#             user.role = "admin"
#             user.is_staff = True

#         user.save()
#         return Response({"role": user.role})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from paths.models import Path
from .permissions import IsAdminRole

User = get_user_model()


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email et mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Identifiants incorrects."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_staff and getattr(user, "role", None) != "admin":
            return Response({"error": "Acces reserve aux administrateurs."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_staff": user.is_staff,
                "role": getattr(user, "role", "participant"),
            }
        }, status=status.HTTP_200_OK)


class SetupAdminView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        secret = request.query_params.get("secret")
        if secret != "tektal2026":
            return Response({"error": "Non autorise"}, status=403)

        user, created = User.objects.get_or_create(
            email="admin@tektal.com",
            defaults={"username": "admin"}
        )
        user.username = "admin"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.role = "admin"
        user.set_password("Admin12345")
        user.save()

        return Response({
            "message": "Admin cree" if created else "Admin mis a jour",
            "role": user.role,
            "is_staff": user.is_staff,
        })


class PathListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        # ✅ Retourne TOUS les parcours sans filtre
        paths = Path.objects.all().order_by('-created_at')
        data = []
        for path in paths:
            steps_data = [
                {
                    "step_number": s.step_number,
                    "text": s.text,
                    "start_time": s.start_time,
                    "end_time": s.end_time,
                }
                for s in path.steps.all()
            ]
            data.append({
                "id": path.id,
                "title": path.title,
                "status": path.status,
                "author": path.user.username,
                "video_url": path.video_url,
                "duration": path.duration,
                "is_official": path.is_official,
                "start_label": path.start_label,
                "end_label": path.end_label,
                "created_at": str(path.created_at),
                "steps": steps_data,
            })
        return Response(data)


class PathDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        steps_data = [
            {
                "step_number": s.step_number,
                "text": s.text,
                "start_time": s.start_time,
                "end_time": s.end_time,
            }
            for s in path.steps.all()
        ]
        return Response({
            "id": path.id,
            "title": path.title,
            "status": path.status,
            "author": path.user.username,
            "video_url": path.video_url,
            "duration": path.duration,
            "is_official": path.is_official,
            "start_label": path.start_label,
            "end_label": path.end_label,
            "created_at": str(path.created_at),
            "steps": steps_data,
        })


class PathApproveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "published"  # ✅ minuscules
        path.save()
        return Response({"status": "published"})


class PathRejectView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "hidden"  # ✅ minuscules
        path.save()
        return Response({"status": "hidden"})


class PublicPathListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # ✅ Retourne uniquement les parcours publiés
        paths = Path.objects.filter(status="published").order_by('-created_at')
        data = [
            {
                "id": p.id,
                "title": p.title,
                "video_url": p.video_url,
                "duration": p.duration,
                "is_official": p.is_official,
                "start_label": p.start_label,
                "end_label": p.end_label,
                "author": p.user.username,
            }
            for p in paths
        ]
        return Response(data)


class ConnectedUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        users = User.objects.filter(is_active=True)
        data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": getattr(user, "role", "user"),
            }
            for user in users
        ]
        return Response(data)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser:
            return Response(
                {"error": "Impossible de supprimer un superadmin."},
                status=status.HTTP_403_FORBIDDEN
            )
        user.delete()
        return Response({"status": "deleted"})


class UserToggleAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user.is_superuser:
            return Response(
                {"error": "Impossible de modifier le superadmin."},
                status=status.HTTP_403_FORBIDDEN
            )

        if user.role == "admin":
            user.role = "participant"
            user.is_staff = False
        else:
            user.role = "admin"
            user.is_staff = True

        user.save()
        return Response({"role": user.role})