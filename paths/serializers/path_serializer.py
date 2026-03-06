# from rest_framework import serializers
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

    # Champs calculés pour la destination automatique
    end_lat = serializers.SerializerMethodField()
    end_lng = serializers.SerializerMethodField()

    class Meta:
        model = Path
        fields = [
            'id', 'share_token', 'title',
            'start_label', 'end_label',        # ✅ ajout
            'start_lat', 'start_lng', 'end_lat', 'end_lng',
            'video_url', 'duration', 'is_official', 'status', 'created_at',
            'steps', 'gps_points'
        ]
        read_only_fields = ['id', 'share_token', 'status', 'is_official', 'created_at', 'end_lat', 'end_lng']

    def get_end_lat(self, obj):
        # Retourne la latitude de l'établissement lié
        if obj.establishment and obj.establishment.lat is not None:
            return obj.establishment.lat
        return None

    def get_end_lng(self, obj):
        # Retourne la longitude de l'établissement lié
        if obj.establishment and obj.establishment.lng is not None:
            return obj.establishment.lng
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
        # tu peux garder ici tes validations supplémentaires si besoin
        return data



# from rest_framework import serializers
# from paths.models import Path, Step


# class StepSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Step
#         fields = ['id', 'step_number', 'start_time', 'end_time', 'text', 'created_at']


# class PathSerializer(serializers.ModelSerializer):
#     steps = StepSerializer(many=True, read_only=True)
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = Path
#         fields = [
#             'id', 'share_token', 'title',
#             'start_label',
#             'start_lat', 'start_lng', 'end_lat', 'end_lng',
#             'video_url', 'duration', 'is_official', 'status', 'created_at',
#             'user', 'steps',
#         ]
#         read_only_fields = [
#             'id', 'share_token', 'status', 'is_official', 'created_at',
#         ]

#     def get_user(self, obj):
#         return {
#             'id': obj.user.id,
#             'name': getattr(obj.user, 'name', '') or getattr(obj.user, 'full_name', ''),
#             'email': obj.user.email,
#         }

#     def validate_duration(self, value):
#         if value > 120:
#             raise serializers.ValidationError(
#                 "La durée de la vidéo ne doit pas dépasser 120 secondes."
#             )
#         if value <= 0:
#             raise serializers.ValidationError(
#                 "La durée de la vidéo doit être supérieure à 0."
#             )
#         return value

#     def validate(self, data):
#         return data