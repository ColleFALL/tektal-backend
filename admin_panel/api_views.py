from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny  # autorise tout le monde pour tester

from .models import Path, Step

# ------------------- Paths API -------------------

class PathListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        paths = Path.objects.all()
        data = []
        for path in paths:
            steps_data = [{"order": s.order, "instruction": s.instruction} for s in path.steps.all()]
            data.append({
                "id": path.id,
                "title": path.title,
                "type_parcours": path.type_parcours,
                "status": path.status,
                "steps": steps_data,
            })
        return Response(data)


class PathDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            path = Path.objects.get(pk=pk)
        except Path.DoesNotExist:
            return Response({"detail": "No Path matches the given query."}, status=status.HTTP_404_NOT_FOUND)
        steps_data = [{"order": s.order, "instruction": s.instruction} for s in path.steps.all()]
        data = {
            "id": path.id,
            "title": path.title,
            "type_parcours": path.type_parcours,
            "status": path.status,
            "steps": steps_data,
        }
        return Response(data)


class PathApproveView(APIView):
    permission_classes = [AllowAny]  # juste pour tester

    def post(self, request, pk):
        try:
            path = Path.objects.get(pk=pk)
        except Path.DoesNotExist:
            return Response({"detail": "No Path matches the given query."}, status=status.HTTP_404_NOT_FOUND)
        path.status = "APPROVED"
        path.save()
        return Response({"status": "approved"})


class PathRejectView(APIView):
    permission_classes = [AllowAny]  # juste pour tester

    def post(self, request, pk):
        try:
            path = Path.objects.get(pk=pk)
        except Path.DoesNotExist:
            return Response({"detail": "No Path matches the given query."}, status=status.HTTP_404_NOT_FOUND)
        path.status = "REJECTED"
        path.save()
        return Response({"status": "rejected"})


# ------------------- Connected Users API -------------------

class ConnectedUsersView(APIView):
    permission_classes = [AllowAny]  # permet de tester sans auth

    def get(self, request):
        # Pour l'instant on liste tous les utilisateurs actifs
        users = User.objects.filter(is_active=True)
        usernames = [user.username for user in users]
        return Response(usernames)
