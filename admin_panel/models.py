from django.db import models
from django.contrib.auth.models import User

class Path(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    campus = models.CharField(max_length=100, default="Général")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Champs spécifiques à l'Admin
    is_official = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    admin_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title