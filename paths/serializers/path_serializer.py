from paths.models import Path, Step
from rest_framework import serializers
from paths.serializers.gps_serializer import GPSPointSerializer

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'step_number', 'start_time', 'end_time', 'text', 'created_at']

class PathSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    gps_points = GPSPointSerializer(many=True, read_only=True)

    end_lat = serializers.SerializerMethodField()
    end_lng = serializers.SerializerMethodField()
    end_label = serializers.SerializerMethodField()

    class Meta:
        model = Path
        fields = [
            'id', 'share_token', 'title',
            'start_label', 'end_label',
            'start_lat', 'start_lng', 'end_lat', 'end_lng',
            'video_url', 'duration', 'is_official', 'status', 'created_at',
            'steps', 'gps_points'
        ]
        read_only_fields = ['id', 'share_token', 'status', 'is_official', 'created_at', 'end_lat', 'end_lng']

    def get_end_lat(self, obj):
        if obj.establishment and obj.establishment.lat is not None:
            return obj.establishment.lat
        return None

    def get_end_lng(self, obj):
        if obj.establishment and obj.establishment.lng is not None:
            return obj.establishment.lng
        return None

    def get_end_label(self, obj):
        if obj.establishment:
            return obj.establishment.name
        return None

    def validate_duration(self, value):
        if value > 120:
            raise serializers.ValidationError("La durée de la vidéo ne doit pas dépasser 120 secondes.")
        if value <= 0:
            raise serializers.ValidationError("La durée de la vidéo doit être supérieure à 0.")
        return value

    def validate(self, data):
        duration = data.get('duration')
        steps = data.get('steps', [])
        return data