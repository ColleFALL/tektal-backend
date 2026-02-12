from django.db import models
from django.conf import settings


class Path(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('hidden', 'Hidden'),
        ('deleted', 'Deleted'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paths'
    )

    title = models.CharField(max_length=255)

    start_label = models.CharField(max_length=255)
    end_label = models.CharField(max_length=255)

    # ⚡ Latitudes et longitudes optionnelles
    start_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    start_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    end_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    end_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    video_url = models.URLField()
    duration = models.PositiveIntegerField(help_text="Duration in seconds")

    is_official = models.BooleanField(default=False)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user})"


class Step(models.Model):
    
    path = models.ForeignKey(
        Path,
        on_delete=models.CASCADE,
        related_name='steps'
    )

    step_number = models.PositiveIntegerField()
    start_time = models.PositiveIntegerField(help_text="Start time in seconds")
    end_time = models.PositiveIntegerField(help_text="End time in seconds")

    text = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step_number']
        unique_together = ('path', 'step_number')

    def __str__(self):
        return f"Step {self.step_number} - {self.path.title}"

# paths/models.py


class SavedPath(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_paths"
    )
    path = models.ForeignKey(
        "Path",
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "path")  # empêche les doublons

    def __str__(self):
        return f"{self.user} -> {self.path.title}"
