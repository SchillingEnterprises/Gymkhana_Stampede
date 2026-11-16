"""Event-domain models with an optional link to Django authentication accounts."""
from django.conf import settings
from django.db import models


class Participant(models.Model):
    """Legacy participant profile; login credentials belong to Django auth."""

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="participant_profile",
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=254)
    birthday = models.DateField()
    # Existing geoposition values were serialized strings. Keep their stored
    # representation so old rows can be preserved without coordinate parsing.
    location = models.CharField(max_length=42, blank=True, default="")
    # upload_to affects future uploads; existing stored file paths are unchanged.
    proof = models.ImageField(upload_to="participants/proofs/", blank=True)

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "participant"
        verbose_name_plural = "participants"

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Checkpoint(models.Model):
    name = models.CharField(max_length=500, default="")
    location = models.CharField(max_length=42, blank=True, default="")
    photograph = models.ImageField(upload_to="checkpoints/", blank=True)
    information = models.TextField(blank=True)
    # New checkpoints start unapproved; existing values are retained by migration.
    is_valid = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=120)
    time = models.DateTimeField()
    location = models.CharField(max_length=42, blank=True, default="")
    # Keep IntegerField to avoid adding a database check constraint that might
    # reject historical values during migration. Validate business rules in forms.
    point_value = models.IntegerField(default=0)

    class Meta:
        ordering = ("time", "name")

    def __str__(self):
        return self.name


class Reward(models.Model):
    # Do not tighten this to PositiveIntegerField until legacy point totals are audited.
    point_total = models.IntegerField(default=0)

    class Meta:
        ordering = ("-point_total",)

    def __str__(self):
        return f"{self.point_total} points"
