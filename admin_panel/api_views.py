from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Path
from .permissions import IsAdminRole

User = get_user_model()

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email et mot de passe requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {"error": "Identifiants incorrects."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_staff and getattr(user, "role", None) != "admin":
            return Response(
                {"error": "Accès réservé aux administrateurs."},
                status=status.HTTP_403_FORBIDDEN
            )

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
            return Response({"error": "Non autorisé"}, status=403)

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
            "message": "Admin créé" if created else "Admin mis à jour",
            "role": user.role,
            "is_staff": user.is_staff,
        })


class PathListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        paths = Path.objects.all()
        data = []
        for path in paths:
            steps_data = [
                {"order": s.order, "instruction": s.instruction}
                for s in path.steps.all()
            ]
            data.append({
                "id": path.id,
                "title": path.title,
                "type_parcours": path.type_parcours,
                "status": path.status,
                "author": path.author.username,
                "steps": steps_data,
                "views": path.views,
                "video_url": path.video_url,
            })
        return Response(data)

    def post(self, request):
        title = request.data.get("title")
        type_parcours = request.data.get("type_parcours")
        video_url = request.data.get("video_url", "")  # ✅ optionnel

        if not title or not type_parcours:
            return Response(
                {"error": "Titre et type sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        path = Path.objects.create(
            title=title,
            type_parcours=type_parcours,
            video_url=video_url,
            author=request.user,
            status="PENDING"
        )
        return Response({
            "id": path.id,
            "title": path.title,
            "status": path.status,
        }, status=status.HTTP_201_CREATED)


class PathDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        steps_data = [
            {"order": s.order, "instruction": s.instruction}
            for s in path.steps.all()
        ]
        return Response({
            "id": path.id,
            "title": path.title,
            "type_parcours": path.type_parcours,
            "status": path.status,
            "author": path.author.username,
            "steps": steps_data,
            "views": path.views,
            "video_url": path.video_url,
        })


class PathApproveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "APPROVED"
        path.save()
        return Response({"status": "approved"})


class PathRejectView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "REJECTED"
        path.save()
        return Response({"status": "rejected"})


class PublicPathListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        paths = Path.objects.filter(status="APPROVED")
        data = [
            {
                "id": p.id,
                "title": p.title,
                "video_url": p.video_url,
                "author": p.author.username,
                "views": p.views,
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
        if user.role == "admin":
            user.role = "participant"
            user.is_staff = False
        else:
            user.role = "admin"
            user.is_staff = True
        user.save()
        return Response({"role": user.role})