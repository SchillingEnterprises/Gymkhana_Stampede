from django.db import models
from geoposition.fields import GeopositionField


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    birthday = models.DateField()
    location = GeopositionField()
    proof = models.ImageField()

    def __str__(self):
        return self.email_address


class Checkpoint(models.Model):
    name = models.CharField(max_length=500)
    location = GeopositionField()
    photograph = models.ImageField()
    information = models.TextField()
    isValid = models.BooleanField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField()
    location = GeopositionField()
    point_value = models.IntegerField()

    def __str__(self):
        return self.name


class Reward(models.Model):
    point_total = models.IntegerField()

    def __str__(self):
        return self.point_total
