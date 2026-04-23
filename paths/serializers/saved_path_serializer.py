# paths/serializers/saved_path_serializer.py
from rest_framework import serializers
from paths.models import SavedPath
from paths.serializers.path_serializer import PathSerializer  # import votre serializer existant

class SavedPathSerializer(serializers.ModelSerializer):
    path = PathSerializer(read_only=True)  #  retourne l'objet complet

    class Meta:
        model = SavedPath
        fields = ['id', 'user', 'path', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']