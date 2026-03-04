from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from paths.models import Establishment

@receiver(post_save, sender=User)
def create_establishment(sender, instance, created, **kwargs):
    if instance.role == 'etablissement':
        Establishment.objects.get_or_create(
            created_by=instance,
            defaults={'name': instance.name}
        )