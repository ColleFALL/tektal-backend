
# from rest_framework import serializers
# from paths.models import Path, Step  # <- ajouté Step

# class StepSerializer(serializers.ModelSerializer):  # <- ajouté
#     class Meta:
#         model = Step
#         fields = ['id', 'step_number', 'start_time', 'end_time', 'text', 'created_at']

# class PathSerializer(serializers.ModelSerializer):
#     steps = StepSerializer(many=True, read_only=True)  # <- ajouté

#     class Meta:
#         model = Path
#         fields = [
#             'id',
#             'title',
#             'start_label',
#             'end_label',
#             'start_lat',
#             'start_lng',
#             'end_lat',
#             'end_lng',
#             'video_url',
#             'duration',
#             'is_official',
#             'status',
#             'created_at',
#             'steps',  # <- ajouté
#         ]
#         read_only_fields = ['id', 'status', 'is_official', 'created_at']
# # 
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
#         def validate(self, data):
#     duration = data.get('duration')
#     steps = data.get('steps', [])

#     for step in steps:
#         if step['end_time'] > duration:
#             raise serializers.ValidationError(
#                 "Une étape ne peut pas dépasser la durée totale de la vidéo."
#             )
#         if step['start_time'] >= step['end_time']:
#             raise serializers.ValidationError(
#                 "Le start_time doit être inférieur au end_time."
#             )
#     return data

from rest_framework import serializers
from paths.models import Path, Step

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'step_number', 'start_time', 'end_time', 'text', 'created_at']

class PathSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)

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
            'steps',
        ]
        read_only_fields = ['id', 'status', 'is_official', 'created_at']

    # Validation de la durée
    def validate_duration(self, value):
        if value > 120:
            raise serializers.ValidationError(
                "La durée de la vidéo ne doit pas dépasser 120 secondes."
            )
        if value <= 0:
            raise serializers.ValidationError(
                "La durée de la vidéo doit être supérieure à 0."
            )
        return value

    # Validation globale des steps
    def validate(self, data):
        duration = data.get('duration')
        steps = data.get('steps', [])

        for step in steps:
            if step['end_time'] > duration:
                raise serializers.ValidationError(
                    "Une étape ne peut pas dépasser la durée totale de la vidéo."
                )
            if step['start_time'] >= step['end_time']:
                raise serializers.ValidationError(
                    "Le start_time doit être inférieur au end_time."
                )
        return data
