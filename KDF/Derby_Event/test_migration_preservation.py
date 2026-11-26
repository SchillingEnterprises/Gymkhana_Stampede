"""Rehearse the legacy-to-current domain migrations on Django's disposable test DB."""

from datetime import date, datetime, timezone

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.exceptions import IrreversibleError
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class LegacyDataPreservationMigrationTests(TransactionTestCase):
    """Prove the profile rename and field conversions retain representative rows."""

    migrate_from = [("Derby_Event", "0001_initial")]
    migrate_to = [("Derby_Event", "0004_guard_participant_account_rollback")]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        LegacyUser = old_apps.get_model("Derby_Event", "User")
        LegacyCheckpoint = old_apps.get_model("Derby_Event", "Checkpoint")
        LegacyEvent = old_apps.get_model("Derby_Event", "Event")
        LegacyReward = old_apps.get_model("Derby_Event", "Reward")

        self.legacy_user = LegacyUser.objects.create(
            first_name="Legacy",
            last_name="Participant",
            email_address="legacy-participant@example.test",
            birthday=date(1988, 4, 12),
            location="38.2560397, -85.8136963",
            proof="legacy/proof.jpg",
        )
        self.legacy_checkpoint = LegacyCheckpoint.objects.create(
            location="38.2625516, -85.8199476",
            photograph="legacy/checkpoint.jpg",
            information="Original checkpoint notes",
        )
        self.legacy_event = LegacyEvent.objects.create(
            name="Original Derby Event",
            time=datetime(2027, 5, 1, 18, 0, tzinfo=timezone.utc),
            location="38.241048, -85.804615",
            point_value=15,
        )
        self.legacy_reward = LegacyReward.objects.create(point_total=-5)

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def tearDown(self):
        # Restore the full current schema for the rest of the test suite.
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_legacy_user_rows_are_renamed_to_participants_without_data_loss(self):
        Participant = self.apps.get_model("Derby_Event", "Participant")
        participant = Participant.objects.get(pk=self.legacy_user.pk)

        self.assertEqual(participant.first_name, "Legacy")
        self.assertEqual(participant.last_name, "Participant")
        self.assertEqual(participant.email_address, "legacy-participant@example.test")
        self.assertEqual(participant.birthday, date(1988, 4, 12))
        self.assertEqual(participant.location, "38.2560397, -85.8136963")
        self.assertEqual(participant.proof, "legacy/proof.jpg")
        self.assertIsNone(participant.account_id)

    def test_checkpoint_fields_are_added_without_rewriting_existing_values(self):
        Checkpoint = self.apps.get_model("Derby_Event", "Checkpoint")
        checkpoint = Checkpoint.objects.get(pk=self.legacy_checkpoint.pk)

        self.assertEqual(checkpoint.location, "38.2625516, -85.8199476")
        self.assertEqual(checkpoint.photograph, "legacy/checkpoint.jpg")
        self.assertEqual(checkpoint.information, "Original checkpoint notes")
        self.assertEqual(checkpoint.name, "")
        self.assertFalse(checkpoint.is_valid)

    def test_event_and_reward_values_survive_domain_migration(self):
        Event = self.apps.get_model("Derby_Event", "Event")
        Reward = self.apps.get_model("Derby_Event", "Reward")
        event = Event.objects.get(pk=self.legacy_event.pk)
        reward = Reward.objects.get(pk=self.legacy_reward.pk)

        self.assertEqual(event.name, "Original Derby Event")
        self.assertEqual(event.point_value, 15)
        self.assertEqual(event.location, "38.241048, -85.804615")
        self.assertEqual(reward.point_total, -5)

    def test_reverse_migration_restores_legacy_user_and_preserves_rows(self):
        """A rollback rehearsal must restore the legacy table without losing data."""
        executor = MigrationExecutor(connection)
        try:
            executor.migrate(self.migrate_from)
            legacy_apps = executor.loader.project_state(self.migrate_from).apps

            LegacyUser = legacy_apps.get_model("Derby_Event", "User")
            LegacyCheckpoint = legacy_apps.get_model("Derby_Event", "Checkpoint")
            LegacyEvent = legacy_apps.get_model("Derby_Event", "Event")
            LegacyReward = legacy_apps.get_model("Derby_Event", "Reward")

            user = LegacyUser.objects.get(pk=self.legacy_user.pk)
            self.assertEqual(user.first_name, "Legacy")
            self.assertEqual(user.last_name, "Participant")
            self.assertEqual(user.email_address, "legacy-participant@example.test")
            self.assertEqual(user.location, "38.2560397, -85.8136963")
            self.assertEqual(user.proof, "legacy/proof.jpg")

            checkpoint = LegacyCheckpoint.objects.get(pk=self.legacy_checkpoint.pk)
            self.assertEqual(checkpoint.location, "38.2625516, -85.8199476")
            self.assertEqual(checkpoint.photograph, "legacy/checkpoint.jpg")
            self.assertEqual(checkpoint.information, "Original checkpoint notes")

            event = LegacyEvent.objects.get(pk=self.legacy_event.pk)
            self.assertEqual(event.name, "Original Derby Event")
            self.assertEqual(event.point_value, 15)

            reward = LegacyReward.objects.get(pk=self.legacy_reward.pk)
            self.assertEqual(reward.point_total, -5)
        finally:
            # Leave the disposable test database at the current schema even if
            # an assertion fails; tearDown also restores the graph's leaf nodes.
            executor = MigrationExecutor(connection)
            executor.migrate(self.migrate_to)

    def test_reverse_migration_blocks_loss_of_participant_account_links(self):
        """Require explicit link export/clearing before reversing the new field."""
        Participant = self.apps.get_model("Derby_Event", "Participant")
        participant = Participant.objects.get(pk=self.legacy_user.pk)
        account = get_user_model().objects.create_user(
            username="synthetic-participant-rollback-link",
            password="unused-test-password",
        )
        participant.account_id = account.pk
        participant.save(update_fields=("account",))

        try:
            executor = MigrationExecutor(connection)
            with self.assertRaisesRegex(IrreversibleError, r"Participant\.account"):
                executor.migrate(self.migrate_from)

            # The failed rollback must be atomic: the association remains usable.
            current_executor = MigrationExecutor(connection)
            current_apps = current_executor.loader.project_state(self.migrate_to).apps
            CurrentParticipant = current_apps.get_model("Derby_Event", "Participant")
            linked_participant = CurrentParticipant.objects.get(pk=self.legacy_user.pk)
            self.assertEqual(linked_participant.account_id, account.pk)

            # Simulate the reviewed export/clear step, then prove rollback succeeds.
            linked_participant.account = None
            linked_participant.save(update_fields=("account",))
            MigrationExecutor(connection).migrate(self.migrate_from)

            legacy_apps = MigrationExecutor(connection).loader.project_state(
                self.migrate_from
            ).apps
            LegacyUser = legacy_apps.get_model("Derby_Event", "User")
            restored_user = LegacyUser.objects.get(pk=self.legacy_user.pk)
            self.assertEqual(restored_user.first_name, "Legacy")
            self.assertEqual(restored_user.email_address, "legacy-participant@example.test")
        finally:
            # The next test always receives the latest migration state.
            MigrationExecutor(connection).migrate(self.migrate_to)
