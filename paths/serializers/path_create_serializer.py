from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step
from paths.serializers.step_serializer import StepSerializer


class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    # ⚡ Rendre les latitudes et longitudes optionnelles
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
            'title',
            'start_label',
            'end_label',
            'start_lat',
            'start_lng',
            'end_lat',
            'end_lng',
            'video_url',
            'duration',
            'steps',
        ]

    # ⚡ Validation du nombre d'étapes
    def validate_steps(self, value):
        if not (2 <= len(value) <= 6):
            raise serializers.ValidationError(
                "Un chemin doit contenir entre 2 et 6 étapes."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])  # <-- sécurisation si pas de steps
        user = self.context['request'].user

        # Crée le chemin
        path = Path.objects.create(user=user, **validated_data)

        # Crée les étapes et injecte le path automatiquement
        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        return path
