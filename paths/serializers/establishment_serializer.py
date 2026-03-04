# paths/serializers/establishment_serializer.py
from rest_framework import serializers
from paths.models import Establishment

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ['id', 'name', 'lat', 'lng', 'created_at']