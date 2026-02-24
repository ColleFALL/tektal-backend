import os
import django

# ⚠️ Remplace config.settings par le chemin exact de tes settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Lecture des variables d'environnement
EMAIL = os.environ.get("ADMIN_EMAIL", "admin@tektal.com")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin12345")

# Crée ou met à jour le superuser
user, created = User.objects.get_or_create(
    email=EMAIL,
    defaults={"username": "admin"}
)

# Forcer toutes les valeurs critiques
user.username = "admin"
user.is_active = True
user.is_staff = True       # 🔥 obligatoire pour admin
user.is_superuser = True    # 🔥 obligatoire
user.role = "admin"         # 🔥 nécessaire pour IsAdminRole
user.set_password(PASSWORD)
user.save()

# Affiche le résultat dans les logs Render
print("===== ADMIN STATUS =====")
print("Admin créé ?" , created)
print("Email      :", user.email)
print("Username   :", user.username)
print("is_active  :", user.is_active)
print("is_staff   :", user.is_staff)
print("is_superuser:", user.is_superuser)
print("role       :", user.role)
print("========================")