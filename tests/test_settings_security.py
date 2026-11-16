"""Source-level security regression tests for Django settings."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = (ROOT / "KDF" / "KDF" / "settings.py").read_text(encoding="utf-8")


class SettingsSecurityTests(unittest.TestCase):
    def test_secret_key_is_environment_driven(self):
        self.assertIn('os.environ.get("DJANGO_SECRET_KEY")', SETTINGS)
        self.assertIn("if not SECRET_KEY:", SETTINGS)
        self.assertNotRegex(SETTINGS, r"(?m)^SECRET_KEY\\s*=\\s*['\\\"]")

    def test_debug_is_disabled_by_default(self):
        self.assertIn('DEBUG = env_bool("DJANGO_DEBUG", False)', SETTINGS)

    def test_hosts_are_environment_driven(self):
        self.assertIn('"DJANGO_ALLOWED_HOSTS"', SETTINGS)
        self.assertIn('"DJANGO_CSRF_TRUSTED_ORIGINS"', SETTINGS)

    def test_google_keys_are_environment_driven_not_hard_coded(self):
        self.assertRegex(SETTINGS, r'GOOGLE_MAPS_BROWSER_API_KEY\\s*=\\s*os\\.environ\\.get\\(')
        self.assertRegex(SETTINGS, r'GOOGLE_API_KEY\\s*=\\s*os\\.environ\\.get\\(')
        self.assertNotRegex(SETTINGS, r"AIza[0-9A-Za-z_-]{20,}")

    def test_production_security_defaults_exist(self):
        for name in ("SECURE_SSL_REDIRECT", "SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE", "SECURE_CONTENT_TYPE_NOSNIFF", "X_FRAME_OPTIONS"):
            with self.subTest(name=name):
                self.assertIn(name, SETTINGS)

    def test_env_example_contains_no_live_key(self):
        example = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("DJANGO_SECRET_KEY=generate-a-long-random-secret", example)
        self.assertNotRegex(example, r"AIza[0-9A-Za-z_-]{20,}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
