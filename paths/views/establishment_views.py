# paths/views/establishment_views.py
from rest_framework import generics, permissions
from paths.models import Establishment
from paths.serializers.establishment_serializer import EstablishmentSerializer

class EstablishmentListView(generics.ListAPIView):
    """
    Liste tous les établissements (destinations possibles)
    """
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # ou AllowAny si public