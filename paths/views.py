from rest_framework import generics, permissions
from paths.models import Path
from paths.serializers.path_create_serializer import PathCreateSerializer


class PathCreateView(generics.CreateAPIView):
    queryset = Path.objects.all()
    serializer_class = PathCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
