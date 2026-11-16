"""Add event checkpoint fields missing from the original initial migration.

Existing checkpoint rows are preserved: name defaults to an empty string and
new checkpoints default to invalid until explicitly reviewed.
"""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Derby_Event", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkpoint",
            name="name",
            field=models.CharField(default="", max_length=500),
        ),
        migrations.AddField(
            model_name="checkpoint",
            name="isValid",
            field=models.BooleanField(default=False),
        ),
    ]
