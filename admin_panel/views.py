from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Path, Step


# =============================
# LISTE DES PARCOURS (ADMIN)
# =============================
class PathListAPI(APIView):

    def get(self, request):
        paths = Path.objects.all().order_by('-created_at')

        data = [
            {
                "id": p.id,
                "title": p.title,
                "type_parcours": p.type_parcours,
                "video_url": p.video_url,
                "status": p.status,
                "author": p.author.username,
                "created_at": p.created_at
            }
            for p in paths
        ]

        return Response(data)

    def post(self, request):
        title = request.data.get("title")
        type_parcours = request.data.get("type_parcours")
        video_url = request.data.get("video_url")
        author_id = request.data.get("author_id")

        if not all([title, video_url, author_id]):
            return Response(
                {"error": "title, video_url et author_id sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=author_id)

        path = Path.objects.create(
            title=title,
            type_parcours=type_parcours,
            video_url=video_url,
            author=user,
            status='PENDING'  # 🔥 Toujours en attente
        )

        return Response(
            {"id": path.id, "message": "Parcours créé en attente de validation."},
            status=status.HTTP_201_CREATED
        )


# =============================
# DETAIL D'UN PARCOURS
# =============================
class PathDetailAPI(APIView):

    def get(self, request, path_id):
        path = get_object_or_404(Path, id=path_id)

        steps_data = [
            {
                "id": s.id,
                "instruction": s.instruction,
                "timestamp": s.timestamp,
                "order": s.order
            }
            for s in path.steps.all()
        ]

        data = {
            "id": path.id,
            "title": path.title,
            "type_parcours": path.type_parcours,
            "video_url": path.video_url,
            "status": path.status,
            "author": path.author.username,
            "steps": steps_data
        }

        return Response(data)

    def delete(self, request, path_id):
        path = get_object_or_404(Path, id=path_id)
        path.delete()
        return Response({"message": "Parcours supprimé."})


# =============================
# ADMIN VALIDE
# =============================
class ApprovePathAPI(APIView):

    def post(self, request, path_id):
        path = get_object_or_404(Path, id=path_id)
        path.status = 'APPROVED'
        path.save()
        return Response({"message": "Parcours validé."})


class RejectPathAPI(APIView):

    def post(self, request, path_id):
        path = get_object_or_404(Path, id=path_id)
        path.status = 'REJECTED'
        path.save()
        return Response({"message": "Parcours refusé."})


# =============================
# PARCOURS 
# =============================
class PublicPathListAPI(APIView):

    def get(self, request):
        paths = Path.objects.filter(status='APPROVED')

        data = [
            {
                "id": p.id,
                "title": p.title,
                "video_url": p.video_url,
                "author": p.author.username
            }
            for p in paths
        ]

        return Response(data)
