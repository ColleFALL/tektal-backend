import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # ⚠️ remplace config.settings si différent
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

EMAIL = os.environ.get("ADMIN_EMAIL", "admin@tektal.com")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin12345")

if not User.objects.filter(email=EMAIL).exists():
    print("Création du superuser...")
    user = User.objects.create(
        email=EMAIL,
        username="admin",
        is_active=True,
        is_staff=True,
        is_superuser=True,
        role="admin"
    )
    user.set_password(PASSWORD)
    user.save()
    print("Superuser créé avec succès.")
else:
    print("Un admin existe déjà.")