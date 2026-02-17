# # paths/views/share_views.py
# from rest_framework import generics, permissions
# from paths.models import Path
# from paths.serializers.path_serializer import PathSerializer
# from django.shortcuts import get_object_or_404

# class SharePathView(generics.RetrieveAPIView):
#     """
#     Endpoint public pour voir un chemin partagé
#     GET /share/<id>/
#     """
#     serializer_class = PathSerializer
#     permission_classes = [permissions.AllowAny]  # public
#     lookup_field = 'id'

#     def get_object(self):
#         # On filtre sur les chemins visibles : published ou officiel
#         return get_object_or_404(Path, id=self.kwargs['id'], status__in=['published', 'hidden'])
from rest_framework import generics, permissions
from paths.models import Path
from paths.serializers.path_serializer import PathSerializer
from django.shortcuts import get_object_or_404

class SharePathView(generics.RetrieveAPIView):
    """
    Endpoint public pour voir un chemin partagé via son token unique.
    GET /share/<uuid:share_token>/
    Accessible sans authentification (published ou hidden).
    """
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'share_token'

    def get_object(self):
        return get_object_or_404(
            Path,
            share_token=self.kwargs['share_token'],
            status__in=['published', 'hidden']
        )