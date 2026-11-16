"""Compatibility field for the original coordinate-string database column.

The legacy GeopositionField stored its value as a varchar(42). The current
domain model intentionally retains that exact text representation. Keeping
this migration-local CharField subclass avoids installing an obsolete runtime
application just to import a historical migration.
"""
from django.db import models


class LegacyGeopositionField(models.CharField):
    description = "Legacy geoposition string"
