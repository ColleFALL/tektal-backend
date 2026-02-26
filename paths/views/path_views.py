
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from paths.models import Path
from paths.serializers.path_create_serializer import PathCreateSerializer
from paths.serializers.path_serializer import PathSerializer
# from paths.serializers.path_create_serializer import PathSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PathCreateView(generics.CreateAPIView):
    serializer_class = PathCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # ✅ PENDING par défaut


class PathListView(generics.ListAPIView):
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Path.objects.filter(status='APPROVED')
        campus_id = self.request.query_params.get('campus_id')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        return queryset.order_by('-created_at')


class PathDetailView(generics.RetrieveAPIView):
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Path.objects.filter(status='APPROVED')