# # paths/views/favorite_views.py
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from paths.models import Path, SavedPath
# from paths.serializers.saved_path_serializer import SavedPathSerializer
# from django.shortcuts import get_object_or_404

# class FavoriteToggleView(generics.GenericAPIView):
#     """
#     POST -> ajoute un favori
#     DELETE -> supprime un favori
#     """
#     serializer_class = SavedPathSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, path_id):
#         path = get_object_or_404(Path, id=path_id, status='published')
#         favorite, created = SavedPath.objects.get_or_create(user=request.user, path=path)
#         if created:
#             return Response({"message": "Favori ajouté"}, status=status.HTTP_201_CREATED)
#         return Response({"message": "Favori déjà existant"}, status=status.HTTP_200_OK)

#     def delete(self, request, path_id):
#         path = get_object_or_404(Path, id=path_id)
#         deleted, _ = SavedPath.objects.filter(user=request.user, path=path).delete()
#         if deleted:
#             return Response({"message": "Favori supprimé"}, status=status.HTTP_204_NO_CONTENT)
#         return Response({"message": "Favori non trouvé"}, status=status.HTTP_404_NOT_FOUND)
 
# class FavoriteListView(generics.ListAPIView):
#     serializer_class = SavedPathSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return SavedPath.objects.filter(user=self.request.user).order_by('-created_at')

# paths/views/favorite_views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from paths.models import Path, SavedPath
from paths.serializers.saved_path_serializer import SavedPathSerializer
from django.shortcuts import get_object_or_404


class FavoriteToggleView(generics.GenericAPIView):
    """
    POST -> ajoute un favori
    DELETE -> supprime un favori
    """
    serializer_class = SavedPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, path_id):
        # ✅ accepte published ET APPROVED
        path = get_object_or_404(Path, id=path_id, status__in=['published', 'APPROVED'])
        favorite, created = SavedPath.objects.get_or_create(user=request.user, path=path)
        if created:
            return Response({"message": "Favori ajouté"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Favori déjà existant"}, status=status.HTTP_200_OK)

    def delete(self, request, path_id):
        path = get_object_or_404(Path, id=path_id)
        deleted, _ = SavedPath.objects.filter(user=request.user, path=path).delete()
        if deleted:
            return Response({"message": "Favori supprimé"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Favori non trouvé"}, status=status.HTTP_404_NOT_FOUND)


class FavoriteListView(generics.ListAPIView):
    serializer_class = SavedPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedPath.objects.filter(user=self.request.user).order_by('-created_at')