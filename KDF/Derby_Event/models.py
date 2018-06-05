from django.db import models
from geoposition.fields import GeopositionField


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    birthday = models.DateField()
    location = GeopositionField()
    proof = models.ImageField()


class Checkpoint(models.Model):
    location = GeopositionField()
    photograph = models.ImageField()
    information = models.TextField()


class Event(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField()
    location = GeopositionField()
    point_value = models.IntegerField()


class Reward(models.Model):
    point_total = models.IntegerField()
