from rest_framework import generics
from django.shortcuts import get_object_or_404, redirect
from paths.models import Path
from paths.serializers.path_serializer import PathSerializer
from rest_framework import generics, permissions

# 🔹 API publique pour récupérer un chemin via share_token
class SharePathView(generics.RetrieveAPIView):
    """
    GET /api/share/<uuid:share_token>/
    Accessible sans authentification
    """
    serializer_class = PathSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "share_token"

    def get_object(self):
        return get_object_or_404(
            Path,
            share_token=self.kwargs["share_token"],
            status__in=["published", "hidden", "APPROVED"],
        )


# 🔹 Redirection publique vers le frontend
class SharePathRedirectView(generics.GenericAPIView):
    """
    GET /share/<uuid:share_token>/
    Redirige vers le frontend
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, share_token):
        get_object_or_404(
            Path,
            share_token=share_token,
            status__in=["published", "hidden", "APPROVED"],
        )
        return redirect(
            f"https://tektal-web-appli.vercel.app/share/{share_token}",
            permanent=False,
        )