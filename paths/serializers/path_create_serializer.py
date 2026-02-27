

# from rest_framework import serializers
# from django.db import transaction
# from paths.models import Path, Step
# from paths.serializers.gps_serializer import GPSPointSerializer


# class StepSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Step
#         fields = ['id', 'step_number', 'start_time', 'end_time', 'text', 'created_at']


# class PathCreateSerializer(serializers.ModelSerializer):
#     steps = StepSerializer(many=True)
#     gps_points = GPSPointSerializer(many=True, required=False)

#     class Meta:
#         model = Path
#         fields = [
#             'id',
#             'share_token',
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
#             'steps',
#             'gps_points',
#         ]
#         read_only_fields = ['id', 'share_token', 'status', 'is_official', 'created_at']

#     def validate_duration(self, value):
#         if value > 120:
#             raise serializers.ValidationError("La durée de la vidéo ne doit pas dépasser 120 secondes.")
#         if value <= 0:
#             raise serializers.ValidationError("La durée de la vidéo doit être supérieure à 0.")
#         return value

#     def validate(self, data):
#         steps = data.get('steps', [])
#         duration = data.get('duration')

#         if not (2 <= len(steps) <= 6):
#             raise serializers.ValidationError("Un chemin doit contenir entre 2 et 6 étapes.")

#         for step in steps:
#             if step['start_time'] >= step['end_time']:
#                 raise serializers.ValidationError("Le start_time doit être inférieur au end_time.")
#             if duration and step['end_time'] > duration:
#                 raise serializers.ValidationError("Une étape ne peut pas dépasser la durée totale.")

#         return data

#     @transaction.atomic
#     def create(self, validated_data):
#         steps_data = validated_data.pop('steps', [])

#         # author et status sont injectés par perform_create dans la vue
#         path = Path.objects.create(**validated_data)
#     @transaction.atomic
#     def create(self, validated_data):
#         steps_data = validated_data.pop('steps', [])
#         gps_points_data = validated_data.pop('gps_points', [])

#         path = Path.objects.create(**validated_data)

# #         for step_data in steps_data:
# #             Step.objects.create(path=path, **step_data)

# #         return path
#         for gps_data in gps_points_data:
#             path.gps_points.create(**gps_data)

#         return path
from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step, GPSPoint
from paths.serializers.step_serializer import StepSerializer
from paths.serializers.gps_serializer import GPSPointSerializer



MAX_VIDEO_DURATION = 120


class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    gps_points = GPSPointSerializer(many=True, required=False)  # ✅ GPS optionnel

    start_lat = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )
    start_lng = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )
    end_lat = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )
    end_lng = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )

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
            'status',
            'is_official',
            'created_at',
            'steps',
            'gps_points',  # ✅ GPS inclus
        ]
        read_only_fields = ['status', 'is_official', 'created_at']

    def validate_duration(self, value):
        if value > MAX_VIDEO_DURATION:
            raise serializers.ValidationError(
                f"La durée de la vidéo ne peut pas dépasser {MAX_VIDEO_DURATION} secondes."
            )
        if value <= 0:
            raise serializers.ValidationError(
                "La durée doit être supérieure à 0."
            )
        return value

    def validate(self, data):
        steps = data.get('steps', [])
        duration = data.get('duration')

        if not (2 <= len(steps) <= 6):
            raise serializers.ValidationError(
                "Un chemin doit contenir entre 2 et 6 étapes."
            )

        for step in steps:
            if step['start_time'] >= step['end_time']:
                raise serializers.ValidationError(
                    "Le start_time doit être inférieur au end_time."
                )
            if duration and step['end_time'] > duration:
                raise serializers.ValidationError(
                    "Une étape ne peut pas dépasser la durée totale de la vidéo."
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        gps_points_data = validated_data.pop('gps_points', [])  # ✅ récupère GPS
        user = self.context['request'].user

        path = Path.objects.create(
            user=user,
            status='draft',
            is_official=False,
            **validated_data
        )

        # ✅ Créer les steps
        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        # ✅ Créer les points GPS avec ordre automatique
        for index, gps_data in enumerate(gps_points_data):
            GPSPoint.objects.create(
                path=path,
                order=index,
                **gps_data
            )

        return path