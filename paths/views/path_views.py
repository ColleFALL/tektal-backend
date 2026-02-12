# from rest_framework import generics, permissions
# from paths.models import Path
# from paths.serializers.path_create_serializer import PathCreateSerializer
# from paths.serializers.path_serializer import PathSerializer  # <- déjà importé

# class PathCreateView(generics.CreateAPIView):
#     serializer_class = PathCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # ⚡ On ne passe plus `user`, le serializer s'en occupe
#         serializer.save(status="draft")  # toujours draft à la création


# class PathListView(generics.ListAPIView):
#     serializer_class = PathSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         return Path.objects.filter(status='published')

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination  # <- ajouté
from paths.models import Path
from paths.serializers.path_create_serializer import PathCreateSerializer
from paths.serializers.path_serializer import PathSerializer

class PathCreateView(generics.CreateAPIView):
    serializer_class = PathCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # ⚡ On ne passe plus `user`, le serializer s'en occupe
        serializer.save(status="draft")  # toujours draft à la création


# ⚡ AJOUT : Pagination standard pour feed
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# ⚡ AJOUT : Feed avec filtre et pagination
class PathListView(generics.ListAPIView):
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination  # <- ajouté

    def get_queryset(self):
        queryset = Path.objects.filter(status='published')
        campus_id = self.request.query_params.get('campus_id')  # <- filtrage facultatif
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        return queryset.order_by('-created_at')  # <- tri par date décroissante


# ⚡ AJOUT : Endpoint détail chemin
class PathDetailView(generics.RetrieveAPIView):
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Path.objects.filter(status='published')
