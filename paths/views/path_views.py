from rest_framework import generics, permissions
from paths.models import Path
from paths.serializers.path_create_serializer import PathCreateSerializer
from paths.serializers.path_serializer import PathSerializer  # <- ajoute cette ligne

class PathCreateView(generics.CreateAPIView):
    serializer_class = PathCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status="draft"  # toujours draft à la création
        )


class PathListView(generics.ListAPIView):
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Path.objects.filter(status='published')
