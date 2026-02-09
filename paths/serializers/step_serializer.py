from rest_framework import serializers
from paths.models import Step, Path


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = [
            'id',
            'path',
            'step_number',
            'start_time',
            'end_time',
            'text',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')

        if start >= end:
            raise serializers.ValidationError(
                "start_time doit être inférieur à end_time pour chaque étape."
            )
        return data
