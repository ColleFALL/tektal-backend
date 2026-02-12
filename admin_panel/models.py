from django.db import models
from django.contrib.auth.models import User

class Path(models.Model):
    TYPE_CHOICES = [
        ('DESTINATION', 'Lieu unique'),
        ('ETAPE', 'Parcours à étapes'),
        ('CHEMIN', 'Itinéraire complet'),
    ]
    title = models.CharField(max_length=255)
    type_parcours = models.CharField(max_length=20, choices=TYPE_CHOICES, default='DESTINATION')
    video_url = models.URLField(max_length=500)
    is_official = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Step(models.Model):
    path = models.ForeignKey(Path, related_name='steps', on_delete=models.CASCADE)
    instruction = models.TextField()
    timestamp = models.IntegerField(help_text="Seconde dans la vidéo")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']