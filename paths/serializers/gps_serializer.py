from rest_framework import serializers
from paths.models import GPSPoint


class GPSPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSPoint
        fields = ['id', 'latitude', 'longitude', 'timestamp', 'order']