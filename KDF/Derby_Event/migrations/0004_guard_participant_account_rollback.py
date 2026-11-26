"""Block rollback when it would discard participant account associations."""

from django.db import migrations
from django.db.migrations.exceptions import IrreversibleError


def refuse_reverse_with_account_links(apps, schema_editor):
    """Keep newer account relationships from disappearing on schema rollback."""
    Participant = apps.get_model("Derby_Event", "Participant")
    has_account_links = (
        Participant.objects.using(schema_editor.connection.alias)
        .filter(account__isnull=False)
        .exists()
    )
    if has_account_links:
        raise IrreversibleError(
            "Cannot reverse the participant-domain migration while "
            "Participant.account links exist. Export and explicitly clear "
            "those links under a reviewed rollback plan first."
        )


class Migration(migrations.Migration):
    dependencies = [
        ("Derby_Event", "0003_participant_domain"),
    ]

    operations = [
        migrations.RunPython(
            migrations.RunPython.noop,
            refuse_reverse_with_account_links,
        ),
    ]
