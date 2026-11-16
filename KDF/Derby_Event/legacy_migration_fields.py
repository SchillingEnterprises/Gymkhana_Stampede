"""Compatibility field for the original coordinate-string migration.

The legacy GeopositionField stored values as varchar(42). The current domain
model retains that exact text representation; no coordinate parsing occurs.
This module is outside migrations/ so Django's migration loader won't mistake
the compatibility class for a migration module.
"""
from django.db import models


class LegacyGeopositionField(models.CharField):
    description = "Legacy geoposition string"
