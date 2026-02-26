from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from paths.models import Path, GPSPoint
from paths.serializers.gps_serializer import GPSPointSerializer


class PathGPSView(APIView):
    """
    GET /api/paths/<path_id>/gps/
    Retourne tous les points GPS d'un chemin.
    Accessible sans authentification pour le web et le mobile.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, path_id):
        path = get_object_or_404(Path, pk=path_id)
        gps_points = GPSPoint.objects.filter(path=path).order_by('order')
        serializer = GPSPointSerializer(gps_points, many=True)
        return Response({
            "path_id": path_id,
            "title": path.title,
            "total_points": gps_points.count(),
            "gps_points": serializer.data
        })