# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
# from djoser.serializers import UserSerializer as BaseUserSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         model = User
#         fields = ("id", "email", "name", "password", "role")
#         extra_kwargs = {
#             "password": {"write_only": True},
#             "name": {"required": False},
#             "role": {"required": False},  # par défaut = participant
#         }

#      def create(self, validated_data):
#      # 🔒 Forcer le rôle à participant
#      validated_data["role"] = "participant"
#      return User.objects.create_user(**validated_data)




# class UserSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         model = User
#         fields = ("id", "email", "name", "role", "is_active", "date_joined")
#         read_only_fields = ("id", "is_active", "date_joined")
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

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

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "role", "is_active", "date_joined")
        read_only_fields = ("id", "is_active", "date_joined")
