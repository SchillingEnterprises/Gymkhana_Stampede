"""Event-domain models; field definitions match the original initial schema.

The local User model is a project profile record, not Django's authentication
user. Authentication users remain managed by django.contrib.auth.
"""
from django.db import models
from geoposition.fields import GeopositionField


class User(models.Model):
    """Legacy event participant profile preserved from migration 0001."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=254)
    birthday = models.DateField()
    location = GeopositionField(max_length=42)
    proof = models.ImageField(upload_to="")

    def __str__(self):
        return self.email_address


class Checkpoint(models.Model):
    name = models.CharField(max_length=500, default="")
    location = GeopositionField(max_length=42)
    photograph = models.ImageField(upload_to="")
    information = models.TextField()
    isValid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField()
    location = GeopositionField(max_length=42)
    point_value = models.IntegerField()

    def __str__(self):
        return self.name


class Reward(models.Model):
    point_total = models.IntegerField()

    def __str__(self):
        return str(self.point_total)
