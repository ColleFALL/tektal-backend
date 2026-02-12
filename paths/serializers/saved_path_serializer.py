# paths/serializers/saved_path_serializer.py
from rest_framework import serializers
from paths.models import SavedPath

class SavedPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPath
        fields = ['id', 'user', 'path', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']
