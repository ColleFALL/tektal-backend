from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step
from paths.serializers.step_serializer import StepSerializer


class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)  # affichage dans la réponse
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

    # Validation du nombre d'étapes
    def validate_steps(self, value):
        if not (2 <= len(value) <= 6):
            raise serializers.ValidationError(
                "Un chemin doit contenir entre 2 et 6 étapes."
            )
        return value

    # Validation de la durée max de la vidéo
    def validate_duration(self, value):
        if value > 45:
            raise serializers.ValidationError(
                "La durée de la vidéo ne peut pas dépasser 45 secondes."
            )
        return value

    # Validation globale pour que les steps respectent la durée max
    def validate(self, data):
        steps = data.get('steps', [])
        if steps:
            max_end_time = max(step['end_time'] for step in steps)
            if max_end_time > 45:
                raise serializers.ValidationError(
                    "Les étapes ne peuvent pas dépasser la durée maximale de 45 secondes."
                )
        return data

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])  # sécurisation
        user = self.context['request'].user

        # Création du Path
        path = Path.objects.create(user=user, **validated_data)

        # Création des steps liés automatiquement
        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        return path
