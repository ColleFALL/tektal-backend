from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")

        email = self.normalize_email(email)

        # username auto si non fourni
        if not extra_fields.get("username"):
            extra_fields["username"] = email.split("@")[0]

        # 🔹 Gestion du role
        role = extra_fields.get("role", "participant")

        # Si admin → staff True
        if role == "admin":
            extra_fields.setdefault("is_staff", True)
        else:
            extra_fields.setdefault("is_staff", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)

    #  NOUVEAU CHAMP ROLE
    ROLE_CHOICES = (
        ("participant", "Participant"),
        ("admin", "Admin"),
        ("etablissement", "Etablissement"),  # 👈 AJOUTER
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="participant"
    )


    # ✅ activation email: user inactif jusqu’à activation
    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
# 🆕 Ajoutez ce modèle
class PasswordResetToken(models.Model):
    """
    Token pour la réinitialisation de mot de passe.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "password_reset_tokens"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reset token for {self.user.email}"

    @classmethod
    def create_for(cls, user, hours=1):
        """
        Crée un token de réinitialisation valide pendant X heures.
        """
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=hours)
        
        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

    def is_valid(self):
        """
        Vérifie si le token est encore valide.
        """
        if self.is_used:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True