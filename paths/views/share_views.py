#  return get_object_or_404(Path, id=self.kwargs['id'], status__in=['published', 'hidden'])
# from rest_framework import generics, permissions
# from paths.models import Path
# from paths.serializers.path_serializer import PathSerializer
# from django.shortcuts import get_object_or_404

# class SharePathView(generics.RetrieveAPIView):
#     """
#     Endpoint public pour voir un chemin partagé via son token unique.
#     GET /share/<uuid:share_token>/
#     Accessible sans authentification (published ou hidden).
#     """
#     serializer_class = PathSerializer
#     permission_classes = [permissions.AllowAny]
#     lookup_field = 'share_token'

#     def get_object(self):
#         return get_object_or_404(
#             Path,
#             share_token=self.kwargs['share_token'],
#             status__in=['published', 'hidden']
#         )

from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, permissions
from rest_framework.views import APIView

from paths.models import Path
from paths.serializers.path_serializer import PathSerializer


class SharePathView(generics.RetrieveAPIView):
    """
    API JSON: GET /api/share/<uuid:share_token>/
    Accessible sans authentification.
    """
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "share_token"

    def get_object(self):
        return get_object_or_404(
            Path,
            share_token=self.kwargs["share_token"],
            status__in=["published", "hidden"],
        )


class SharePathRedirectView(APIView):
    """
    Redirection publique: GET /share/<uuid:share_token>/
    Redirige vers le frontend web Vercel.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, share_token):
        # Validation: le token doit exister et être partageable
        get_object_or_404(
            Path,
            share_token=share_token,
            status__in=["published", "hidden"],
        )

        return redirect(
            f"https://tektal-web-appli.vercel.app/share/{share_token}",
            permanent=False,  # 302
        )