import os
import django

# ⚠️ Remplace config.settings par le chemin correct de tes settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Lecture des variables d'environnement
EMAIL = os.environ.get("ADMIN_EMAIL", "admin@tektal.com")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin12345")

# Récupérer ou créer le superuser
user, created = User.objects.get_or_create(
    email=EMAIL,
    defaults={"username": "admin"}
)

# Forcer toutes les valeurs critiques, même si le compte existait déjà
user.username = "admin"
user.is_active = True
user.is_staff = True       # ✅ nécessaire pour accéder au Django Admin
user.is_superuser = True    # ✅ superuser
user.role = "admin"         # ✅ nécessaire pour IsAdminRole
user.set_password(PASSWORD)
user.save()

print("Admin créé." if created else "Admin mis à jour avec succès.")