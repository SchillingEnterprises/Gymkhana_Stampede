"""Source-level checks for the supported Gymkhana runtime contract."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SupportedRuntimeTests(unittest.TestCase):
    def test_active_requirements_are_small_and_supported(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        for dependency in ("Django==6.1.3", "django-allauth==65.22.1", "Pillow==13.0.0",
                           "gunicorn==23.0.0", "psycopg[binary]==3.3.9"):
            with self.subTest(dependency=dependency):
                self.assertIn(dependency, requirements)
        for obsolete in ("Django==2.2.10", "django-geoposition", "tensorflow", "notebook=="):
            self.assertNotIn(obsolete, requirements)

    def test_settings_use_supported_allauth_and_optional_postgres(self):
        settings = (ROOT / "KDF/KDF/settings.py").read_text(encoding="utf-8")
        self.assertIn("allauth.account.middleware.AccountMiddleware", settings)
        self.assertIn('ACCOUNT_SIGNUP_ENABLED = False', settings)
        self.assertIn('DJANGO_DB_ENGINE', settings)
        self.assertIn('django.db.backends.postgresql', settings)
        self.assertNotIn("'geoposition',", settings)
        self.assertNotIn("'allauth_bootstrap',", settings)
        self.assertNotIn("'bootstrapform',", settings)

    def test_app_engine_uses_real_wsgi_module_and_supported_runtime(self):
        config = (ROOT / "app.yaml").read_text(encoding="utf-8")
        self.assertIn("runtime: python312", config)
        self.assertIn("KDF.wsgi:application", config)
        self.assertNotIn("mysite.wsgi", config)
        self.assertNotIn("<your-cloudsql-connection-string>", config)

    def test_legacy_migration_keeps_coordinate_storage_as_varchar(self):
        migration = (ROOT / "KDF/Derby_Event/migrations/0001_initial.py").read_text(encoding="utf-8")
        field = (ROOT / "KDF/Derby_Event/legacy_migration_fields.py").read_text(encoding="utf-8")
        self.assertIn("LegacyGeopositionField(max_length=42)", migration)
        self.assertIn("models.CharField", field)
        self.assertNotIn("import geoposition.fields", migration)

    def test_optional_upload_adapter_has_no_import_time_sdk_dependency_or_secrets(self):
        upload = (ROOT / "KDF/Derby_Event/upload.py").read_text(encoding="utf-8")
        self.assertIn("def upload_file", upload)
        self.assertIn("import easyapiio", upload)
        self.assertNotIn("YOUR_API_KEY", upload)
        self.assertNotIn("if not results", upload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
