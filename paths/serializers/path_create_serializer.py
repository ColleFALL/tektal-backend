# from rest_framework import serializers
# from django.db import transaction
# from paths.models import Path, Step
# from paths.serializers.step_serializer import StepSerializer


# class PathCreateSerializer(serializers.ModelSerializer):
#     # Nested serializer normal pour créer et afficher les steps
#     steps = StepSerializer(many=True)

#     # Lat/Lng optionnelles
#     start_lat = serializers.DecimalField(
#         max_digits=9, decimal_places=6, required=False, allow_null=True
#     )
#     start_lng = serializers.DecimalField(
#         max_digits=9, decimal_places=6, required=False, allow_null=True
#     )
#     end_lat = serializers.DecimalField(
#         max_digits=9, decimal_places=6, required=False, allow_null=True
#     )
#     end_lng = serializers.DecimalField(
#         max_digits=9, decimal_places=6, required=False, allow_null=True
#     )

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
#             'status',
#             'is_official',
#             'created_at',
#             'steps',
#         ]

#     # Validation du nombre d'étapes
#     def validate_steps(self, value):
#         if not (2 <= len(value) <= 6):
#             raise serializers.ValidationError(
#                 "Un chemin doit contenir entre 2 et 6 étapes."
#             )
#         # Vérifie que chaque step ne dépasse pas 45s
#         for step in value:
#             if step['end_time'] > 45:
#                 raise serializers.ValidationError(
#                     "Chaque étape doit se situer dans les 45 secondes de la vidéo."
#                 )
#         return value

#     # Validation de la durée max de la vidéo
#     def validate_duration(self, value):
#         if value > 45:
#             raise serializers.ValidationError(
#                 "La durée de la vidéo ne peut pas dépasser 45 secondes."
#             )
#         return value

#     @transaction.atomic
#     def create(self, validated_data):
#         # On récupère et supprime les steps pour créer le Path
#         steps_data = validated_data.pop('steps', [])
#         user = self.context['request'].user

#         # Création du Path
#         path = Path.objects.create(user=user, **validated_data)

#         # Création des steps liés automatiquement
#         for step_data in steps_data:
#             Step.objects.create(path=path, **step_data)

#         # Recharge les steps pour les afficher dans la réponse
#         path.steps.set(path.steps.all())

#         return path
from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step
from paths.serializers.step_serializer import StepSerializer


MAX_VIDEO_DURATION = 120


class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    # Lat/Lng optionnelles
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
        ]
        read_only_fields = ['status', 'is_official', 'created_at']

    # Validation durée vidéo
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

    # Validation globale (steps + cohérence avec duration)
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
        user = self.context['request'].user

        # Forcer sécurité
        path = Path.objects.create(
            user=user,
            status='published',
            is_official=False,
            **validated_data
        )

        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        return path
