
# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
# from djoser.serializers import UserSerializer as BaseUserSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class UserCreateSerializer(BaseUserCreateSerializer):
#     """Création utilisateur (name + email + password)"""

#     class Meta(BaseUserCreateSerializer.Meta):
#         model = User
#         fields = ("id", "email", "name", "password", "role")
#         extra_kwargs = {
#             "password": {"write_only": True},
#             "name": {"required": False},
#             "role": {"required": False},
#         }

#     def create(self, validated_data):
#         validated_data["role"] = "participant"
#         return User.objects.create_user(**validated_data)


# class UserSerializer(BaseUserSerializer):
#     """Retour profil utilisateur"""

#     class Meta(BaseUserSerializer.Meta):
#         model = User
#         fields = ("id", "email", "name", "role", "is_active", "date_joined")
#         read_only_fields = ("id", "is_active", "date_joined")
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """Création utilisateur (name + email + password)"""

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "password", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "name": {"required": False},
            "role": {"required": False},
        }

    def create(self, validated_data):
        validated_data["role"] = "participant"
        return User.objects.create_user(**validated_data)


class UserSerializer(BaseUserSerializer):
    """Retour profil utilisateur"""
    establishment_name = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "role", "is_active", "date_joined", "establishment_name")
        read_only_fields = ("id", "is_active", "date_joined")

    def get_establishment_name(self, obj):
    try:
        return obj.establishment.name  # related_name = 'establishment' dans paths/models.py
    except:
        return None