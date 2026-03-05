from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from paths.models import Establishment

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, default="participant")
    establishment_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "name", "password", "role", "establishment_name")

    def create(self, validated_data):
        establishment_name = validated_data.pop("establishment_name", None)
        role = validated_data.get("role", "participant")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data.get("username") or validated_data["email"].split("@")[0],
            name=validated_data.get("name", ""),
            role=role,
            is_active=True,  # ✅ actif directement
        )

        # ✅ Créer l'objet Establishment si rôle = etablissement
        if role == "etablissement" and establishment_name:
            Establishment.objects.create(
                name=establishment_name,
                created_by=user,
            )

        return user


class UserCreateSerializer(BaseUserCreateSerializer):
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
    establishment_name = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "name", "role", "is_active", "date_joined", "establishment_name")
        read_only_fields = ("id", "is_active", "date_joined")

    def get_establishment_name(self, obj):
        try:
            return obj.etablissement.name  # ✅ related_name = 'etablissement'
        except:
            return None