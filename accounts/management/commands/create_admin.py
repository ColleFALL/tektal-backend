# create_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée un admin par défaut'

    def handle(self, *args, **kwargs):
        email = "admin@tektal.com"
        password = "Admin1234!"

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"⚠️  Admin {email} existe déjà")
            return

        user = User.objects.create_user(
            email=email,
            password=password,
            role="admin",
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(f"Admin créé : {email}")