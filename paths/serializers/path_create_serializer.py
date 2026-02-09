from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step
from paths.serializers.step_serializer import StepSerializer


class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)  # liste des étapes

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

    def validate_steps(self, value):
        if not (2 <= len(value) <= 6):
            raise serializers.ValidationError(
                "Un chemin doit contenir entre 2 et 6 étapes."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        user = self.context['request'].user

        # Crée le chemin
        path = Path.objects.create(user=user, **validated_data)

        # Crée les étapes
        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        return path
