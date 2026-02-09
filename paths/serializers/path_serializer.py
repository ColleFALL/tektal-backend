from rest_framework import serializers
from paths.models import Path


class PathSerializer(serializers.ModelSerializer):

    class Meta:
        model = Path
        fields = [
            'id',
            'title',
            'start_label',
            'end_label',
            'start_lat',
            'start_lng',
            'end_lat',
            'end_lng',
            'video_url',
            'duration',
            'is_official',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'is_official', 'created_at']

    def validate_duration(self, value):
        if value > 45:
            raise serializers.ValidationError(
                "La durée de la vidéo ne doit pas dépasser 45 secondes."
            )
        if value <= 0:
            raise serializers.ValidationError(
                "La durée de la vidéo doit être supérieure à 0."
            )
        return value
