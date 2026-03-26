

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from paths.models import Path
from .permissions import IsAdminRole
from paths.models import Establishment

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

        if not user.is_staff and getattr(user, "role", None) not in ["admin", "etablissement"]:
            return Response({"error": "Acces reserve aux administrateurs ou etablissement."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,  # ✅ AJOUTÉ
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
                "author_role": path.user.role,
                "video_url": path.video_url,
                "duration": path.duration,
                "is_official": path.is_official,
                "start_label": path.start_label,
                "end_label": path.establishment.name if path.establishment else None,
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
            "end_label": path.establishment.name if path.establishment else None,
            "created_at": str(path.created_at),
            "steps": steps_data,
        })


class PathApproveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "published"
        path.save()
        return Response({"status": "published"})


class PathRejectView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "hidden"
        path.save()
        return Response({"status": "hidden"})


class PublicPathListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        paths = Path.objects.filter(status="published").order_by('-created_at')
        data = [
            {
                "id": p.id,
                "title": p.title,
                "video_url": p.video_url,
                "duration": p.duration,
                "is_official": p.is_official,
                "start_label": p.start_label,
                "end_label": p.establishment.name if p.establishment else None,
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
                "is_superuser": user.is_superuser,  # ✅ AJOUTÉ
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

        role = request.data.get("role")
        if role not in ["admin", "etablissement", "participant"]:
            return Response({"error": "Rôle invalide. Choisir 'admin', 'establishment' ou 'participant'."}, 
             status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.is_staff = True if role == "admin" else False
        user.save()

        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "is_staff": user.is_staff
        })


class EtablissementListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        etablissements = User.objects.filter(role='etablissement')
        data = []
        for e in etablissements:
            try:
                establishment = e.etablissement
                lat = str(establishment.lat) if establishment.lat else None
                lng = str(establishment.lng) if establishment.lng else None
                name = establishment.name
                total_paths = establishment.paths.count()
            except:
                lat = None
                lng = None
                name = e.username
                total_paths = 0

            data.append({
                "id": e.id,
                "name": name,
                "username": e.username,
                "user_email": e.email,
                "lat": lat,
                "lng": lng,
                "total_paths": total_paths,
                "created_at": str(e.date_joined),
            })
        return Response(data)


class EtablissementDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def delete(self, request, pk):
        etab = get_object_or_404(User, pk=pk, role='etablissement')
        etab.delete()
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


class EtablissementProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            establishment = request.user.etablissement
            return Response({
                "id": establishment.id,
                "name": establishment.name,
                "lat": str(establishment.lat) if establishment.lat else None,
                "lng": str(establishment.lng) if establishment.lng else None,
            })
        except:
            return Response({"error": "Etablissement non trouve."}, status=404)


class EtablissementPathListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            establishment = request.user.etablissement
            paths = Path.objects.filter(establishment=establishment).order_by('-created_at')
        except:
            paths = Path.objects.filter(user=request.user).order_by('-created_at')

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
                "end_label": path.establishment.name if path.establishment else None,
                "created_at": str(path.created_at),
                "steps": steps_data,
            })
        return Response(data)


class EtablissementPathApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "published"
        path.save()
        return Response({"status": "published"})


class EtablissementPathRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "hidden"
        path.save()
        return Response({"status": "hidden"})


class UserToggleEtablissementView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user.is_superuser:
            return Response(
                {"error": "Impossible de modifier le superadmin."},
                status=status.HTTP_403_FORBIDDEN
            )

        if user.role == "etablissement":
            user.role = "participant"
            user.is_staff = False
        else:
            user.role = "etablissement"
            user.is_staff = False

        user.save()
        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
        })
class PathDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def delete(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        path.status = "deleted"
        path.save()
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


class PathHideView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)
        if path.status == "hidden":
            path.status = "published"  # toggle : si déjà caché → republier
            message = "published"
        else:
            path.status = "hidden"
            message = "hidden"
        path.save()
        return Response({"status": message}, status=status.HTTP_200_OK)  

class EtablissementPathDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        path = get_object_or_404(Path, pk=pk)

        # Vérifie que le chemin appartient bien à son établissement
        try:
            establishment = request.user.etablissement
            if path.establishment != establishment:
                return Response(
                    {"error": "Action non autorisée sur ce chemin."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            return Response(
                {"error": "Etablissement non trouvé."},
                status=status.HTTP_403_FORBIDDEN
            )

        path.status = "deleted"
        path.save()
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


class EtablissementPathHideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        path = get_object_or_404(Path, pk=pk)

        # Vérifie que le chemin appartient bien à son établissement
        try:
            establishment = request.user.etablissement
            if path.establishment != establishment:
                return Response(
                    {"error": "Action non autorisée sur ce chemin."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            return Response(
                {"error": "Etablissement non trouvé."},
                status=status.HTTP_403_FORBIDDEN
            )

        if path.status == "hidden":
            path.status = "published"
            message = "published"
        else:
            path.status = "hidden"
            message = "hidden"

        path.save()
        return Response({"status": message}, status=status.HTTP_200_OK)