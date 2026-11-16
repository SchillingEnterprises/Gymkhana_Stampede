"""Convert the legacy event User profile to Participant without dropping rows."""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Derby_Event", "0002_checkpoint_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Rename the existing profile model/table; do not create a replacement
        # table or discard any participant rows.
        migrations.RenameModel(
            old_name="User",
            new_name="Participant",
        ),
        migrations.AddField(
            model_name="participant",
            name="account",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="participant_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        # GeoPositionField stored coordinate strings. CharField retains those
        # values as text; no geocoding or coordinate transformation is performed.
        migrations.AlterField(
            model_name="participant",
            name="location",
            field=models.CharField(blank=True, default="", max_length=42),
        ),
        # upload_to affects only future upload paths; existing DB file names remain.
        migrations.AlterField(
            model_name="participant",
            name="proof",
            field=models.ImageField(blank=True, upload_to="participants/proofs/"),
        ),
        migrations.RenameField(
            model_name="checkpoint",
            old_name="isValid",
            new_name="is_valid",
        ),
        migrations.AlterField(
            model_name="checkpoint",
            name="is_valid",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="checkpoint",
            name="location",
            field=models.CharField(blank=True, default="", max_length=42),
        ),
        migrations.AlterField(
            model_name="checkpoint",
            name="photograph",
            field=models.ImageField(blank=True, upload_to="checkpoints/"),
        ),
        migrations.AlterField(
            model_name="checkpoint",
            name="information",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="name",
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.CharField(blank=True, default="", max_length=42),
        ),
        migrations.AlterField(
            model_name="event",
            name="point_value",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="reward",
            name="point_total",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name="participant",
            options={
                "ordering": ("last_name", "first_name"),
                "verbose_name": "participant",
                "verbose_name_plural": "participants",
            },
        ),
        migrations.AlterModelOptions(
            name="checkpoint",
            options={"ordering": ("name",)},
        ),
        migrations.AlterModelOptions(
            name="event",
            options={"ordering": ("time", "name")},
        ),
        migrations.AlterModelOptions(
            name="reward",
            options={"ordering": ("-point_total",)},
        ),
    ]
