
# from django.db import models
# from django.conf import settings
# import uuid


# class Path(models.Model):
#     STATUS_CHOICES = (
#         ('draft', 'Draft'),
#         ('published', 'Published'),
#         ('hidden', 'Hidden'),
#         ('deleted', 'Deleted'),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='paths'
#     )

#     title = models.CharField(max_length=255)

#     start_label = models.CharField(max_length=255)
#     end_label = models.CharField(max_length=255)

#     start_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     start_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     end_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     end_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

#     video_url = models.URLField()
#     duration = models.PositiveIntegerField(help_text="Duration in seconds")

#     is_official = models.BooleanField(default=False)

#     status = models.CharField(
#         max_length=10,
#         choices=STATUS_CHOICES,
#         default='draft'
#     )

#     share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} ({self.user})"


# class Step(models.Model):
#     path = models.ForeignKey(
#         Path,
#         on_delete=models.CASCADE,
#         related_name='steps'
#     )

#     step_number = models.PositiveIntegerField()
#     start_time = models.PositiveIntegerField(help_text="Start time in seconds")
#     end_time = models.PositiveIntegerField(help_text="End time in seconds")

#     text = models.CharField(max_length=255)

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['step_number']
#         unique_together = ('path', 'step_number')

#     def __str__(self):
#         return f"Step {self.step_number} - {self.path.title}"


# class SavedPath(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="saved_paths"
#     )
#     path = models.ForeignKey(
#         "Path",
#         on_delete=models.CASCADE,
#         related_name="saved_by"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("user", "path")

#     def __str__(self):
#         return f"{self.user} -> {self.path.title}"


# #  NOUVEAU : Points GPS du trajet
# class GPSPoint(models.Model):
#     path = models.ForeignKey(
#         Path,
#         on_delete=models.CASCADE,
#         related_name='gps_points'
#     )
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     timestamp = models.BigIntegerField(help_text="Timestamp en millisecondes")
#     order = models.PositiveIntegerField(help_text="Ordre du point GPS dans le trajet")

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f"GPS Point {self.order} - {self.path.title}"
from django.db import models
from django.conf import settings
import uuid

# 🔹 Modèle des établissements
class Establishment(models.Model):
    name = models.CharField(max_length=255)  # Nom obligatoire à l'inscription
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Coordonnées facultatives
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='etablissement'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 🔹 Chemins (Paths)
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

    # Lien obligatoire vers un établissement
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='paths',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)

    # Départ libre pour établissement ou participant (facultatif)
    start_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    start_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Destination = coordonnées de l'établissement (facultatif si l'établissement ne les a pas renseignées)
    end_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    end_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    video_url = models.URLField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in seconds", null=True, blank=True)

    # Indique si le Path est officiel (créé par l'établissement ou admin)
    is_official = models.BooleanField(default=False)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.establishment})"


# 🔹 Étapes d’un chemin
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


# 🔹 Chemins sauvegardés par un participant
class SavedPath(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_paths"
    )
    path = models.ForeignKey(
        Path,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "path")

    def __str__(self):
        return f"{self.user} -> {self.path.title}"


# 🔹 Points GPS
class GPSPoint(models.Model):
    path = models.ForeignKey(
        Path,
        on_delete=models.CASCADE,
        related_name='gps_points'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.BigIntegerField(help_text="Timestamp en millisecondes")
    order = models.PositiveIntegerField(help_text="Ordre du point GPS dans le trajet")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"GPS Point {self.order} - {self.path.title}"
