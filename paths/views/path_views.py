
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.db import models
from paths.models import Path
from paths.serializers.path_create_serializer import PathCreateSerializer
from paths.serializers.path_serializer import PathSerializer

# 🔹 Pagination standard
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# 🔹 Création d'un chemin (Path)
class PathCreateView(generics.CreateAPIView):
    """
    Crée un chemin pour :
    - un établissement : le champ establishment est automatiquement lié
    - un admin : doit fournir l'établissement dans la requête
    """
    serializer_class = PathCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        establishment = getattr(user, 'etablissement', None)
        serializer.save(user=user, establishment=establishment)


# 🔹 Liste des chemins
class PathListView(generics.ListAPIView):
    """
    Liste des chemins selon le rôle :
    - Admin : tout voir
    - Établissement : ses propres + publiés
    - Participant/visiteur : seulement publiés
    """
    serializer_class = PathSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = Path.objects.all().order_by('-created_at')
        elif hasattr(user, 'etablissement'):
            queryset = Path.objects.filter(
                models.Q(user=user) | models.Q(status='published')
            ).order_by('-created_at')
        else:
            queryset = Path.objects.filter(status='published').order_by('-created_at')

        # Filtre optionnel par établissement
        establishment_id = self.request.query_params.get('establishment_id')
        if establishment_id:
            queryset = queryset.filter(establishment_id=establishment_id)

        return queryset


# 🔹 Détail d'un chemin
class PathDetailView(generics.RetrieveAPIView):
    """
    Détail d'un chemin selon le rôle :
    - Participant/visiteur : seulement si status='published'
    - Établissement/admin : tout voir
    """
    serializer_class = PathSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Path.objects.all()
        elif hasattr(user, 'etablissement'):
            return Path.objects.filter(
                models.Q(user=user) | models.Q(status='published')
            )
        return Path.objects.filter(status='published')