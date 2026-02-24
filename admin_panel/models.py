from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ('PENDING', 'En attente'),
    ('APPROVED', 'Validé'),
    ('REJECTED', 'Refusé'),
]

TYPE_CHOICES = [
    ('DESTINATION', 'Destination'),
    ('ACTIVITY', 'Activité'),
]

class Path(models.Model):
    title = models.CharField(max_length=255)
    type_parcours = models.CharField(max_length=50, choices=TYPE_CHOICES)
    video_url = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)  # ✅ upload fichier
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Step(models.Model):
    path = models.ForeignKey(Path, on_delete=models.CASCADE, related_name='steps')
    instruction = models.TextField()
    order = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.path.title} - Step {self.order}"