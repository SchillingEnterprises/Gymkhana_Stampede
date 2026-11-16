"""Core domain models for the Gymkhana Stampede event experience."""
from django.conf import settings
from django.db import models


class Participant(models.Model):
    """A participant profile linked to Django's built-in authentication account."""

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="participant_profile",
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    birthday = models.DateField()
    # The original project stored coordinates as a serialized string. Keep that
    # representation so existing rows survive the migration; new map fields can
    # be introduced separately after the historic values have been audited.
    location = models.CharField(max_length=42, blank=True, default="")
    proof = models.ImageField(upload_to="participants/proofs/", blank=True)

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "participant"
        verbose_name_plural = "participants"

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Checkpoint(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=42, blank=True, default="")
    photograph = models.ImageField(upload_to="checkpoints/", blank=True)
    information = models.TextField(blank=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=120)
    time = models.DateTimeField()
    location = models.CharField(max_length=42, blank=True, default="")
    point_value = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("time", "name")

    def __str__(self):
        return self.name


class Reward(models.Model):
    point_total = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-point_total",)

    def __str__(self):
        return f"{self.point_total} points"
