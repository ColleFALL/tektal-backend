from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Path
from .permissions import IsAdminRole



#  PATHS ADMIN (PROTÉGÉ)
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
            })

        return Response(data)


class PathDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, pk):
        path = get_object_or_404(Path, pk=pk)

        steps_data = [
            {"order": s.order, "instruction": s.instruction}
            for s in path.steps.all()
        ]

        data = {
            "id": path.id,
            "title": path.title,
            "type_parcours": path.type_parcours,
            "status": path.status,
            "author": path.author.username,
            "steps": steps_data,
        }

        return Response(data)


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



#  PATHS PUBLICS
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
            }
            for p in paths
        ]

        return Response(data)



#  UTILISATEURS CONNECTÉS (ADMIN)
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
