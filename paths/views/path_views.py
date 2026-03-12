from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.db import models
from paths.models import Path, Establishment
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

        # Si établissement → lier automatiquement
        establishment = getattr(user, 'etablissement', None)

        # Si admin → récupérer l'establishment_id envoyé dans la requête
        if not establishment and user.is_staff:
            establishment_id = self.request.data.get('establishment')
            if establishment_id:
                try:
                    establishment = Establishment.objects.get(id=establishment_id)
                except Establishment.DoesNotExist:
                    establishment = None

        serializer.save(user=user, establishment=establishment)


# 🔹 Liste des chemins
class PathListView(generics.ListAPIView):
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

        establishment_id = self.request.query_params.get('establishment_id')
        if establishment_id:
            queryset = queryset.filter(establishment_id=establishment_id)

        return queryset


# 🔹 Détail d'un chemin
class PathDetailView(generics.RetrieveAPIView):
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