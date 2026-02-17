# admin_panel/serializers.py
from rest_framework import serializers
from .models import Path, Step
from django.contrib.auth import get_user_model

User = get_user_model()

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

class PathSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    class Meta:
        model = Path
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
