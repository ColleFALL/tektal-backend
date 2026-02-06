from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """Création utilisateur (name + email + password)"""
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "name": {"required": False},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(BaseUserSerializer):
    """Retour profil utilisateur"""
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "is_active", "date_joined")
        read_only_fields = ("id", "is_active", "date_joined")
