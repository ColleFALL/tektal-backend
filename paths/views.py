# from rest_framework import generics, permissions
# from paths.models import Path
# from paths.serializers.path_create_serializer import PathCreateSerializer
# # from paths.serializers.path_serializer import PathSerializer


# class PathCreateView(generics.CreateAPIView):
#     queryset = Path.objects.all()
#     serializer_class = PathCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class PathListView(generics.ListAPIView):
#     serializer_class = PathSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         return Path.objects.filter(status='published')
