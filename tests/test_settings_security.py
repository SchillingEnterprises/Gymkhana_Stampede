"""Source-level security regression tests for Django settings."""
from pathlib import Path
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = (ROOT / "KDF" / "KDF" / "settings.py").read_text(encoding="utf-8")


class SettingsSecurityTests(unittest.TestCase):
    def test_secret_key_is_environment_driven(self):
        self.assertIn('SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")', SETTINGS)
        self.assertIn("if not SECRET_KEY", SETTINGS)
        self.assertIn("len(SECRET_KEY) < 50", SETTINGS)
        self.assertIn("len(set(SECRET_KEY)) < 5", SETTINGS)

    def test_short_and_low_diversity_secret_keys_fail_closed(self):
        weak_keys = (
            ("short-secret", "at least 50 characters"),
            (("A" * 59) + "b", "5 distinct characters"),
        )
        for weak_key, expected_message in weak_keys:
            with self.subTest(weak_key=weak_key[:8]):
                env = os.environ.copy()
                env.update({
                    "DJANGO_SETTINGS_MODULE": "KDF.settings",
                    "DJANGO_SECRET_KEY": weak_key,
                    "DJANGO_DEBUG": "true",
                    "PYTHONPATH": str(ROOT / "KDF"),
                })
                result = subprocess.run(
                    [sys.executable, "-c", "from django.conf import settings; print(settings.SECRET_KEY)"],
                    cwd=ROOT / "KDF",
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_message, result.stderr)

    def test_valid_high_diversity_secret_key_is_accepted(self):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "KDF.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key-with-at-least-fifty-characters-and-varied-alphabet",
            "DJANGO_DEBUG": "true",
            "PYTHONPATH": str(ROOT / "KDF"),
        })
        result = subprocess.run(
            [sys.executable, "-c", "from django.conf import settings; assert len(settings.SECRET_KEY) >= 50"],
            cwd=ROOT / "KDF",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_debug_is_disabled_by_default(self):
        self.assertIn('DEBUG = env_bool("DJANGO_DEBUG", False)', SETTINGS)

    def test_hosts_are_environment_driven(self):
        self.assertIn('"DJANGO_ALLOWED_HOSTS"', SETTINGS)
        self.assertIn('"DJANGO_CSRF_TRUSTED_ORIGINS"', SETTINGS)

    def test_google_keys_are_environment_driven_not_hard_coded(self):
        self.assertIn('GOOGLE_MAPS_BROWSER_API_KEY = os.environ.get("GOOGLE_MAPS_BROWSER_API_KEY", "")', SETTINGS)
        self.assertIn('GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")', SETTINGS)
        self.assertNotIn("AIza", SETTINGS)

    def test_production_security_defaults_exist(self):
        for name in ("SECURE_SSL_REDIRECT", "SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE", "SECURE_CONTENT_TYPE_NOSNIFF", "X_FRAME_OPTIONS"):
            with self.subTest(name=name):
                self.assertIn(name, SETTINGS)

    def test_invalid_boolean_security_settings_fail_closed(self):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "KDF.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key-with-at-least-fifty-characters-and-varied-alphabet",
            "DJANGO_DEBUG": "tru",
            "PYTHONPATH": str(ROOT / "KDF"),
        })
        result = subprocess.run(
            [sys.executable, "-c", "from django.conf import settings; print(settings.DEBUG)"],
            cwd=ROOT / "KDF",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_DEBUG must be an explicit boolean value", result.stderr)

    def test_explicit_false_boolean_values_are_supported(self):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "KDF.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key-with-at-least-fifty-characters-and-varied-alphabet",
            "DJANGO_DEBUG": "false",
            "DJANGO_SECURE_SSL_REDIRECT": "off",
            "DJANGO_SESSION_COOKIE_SECURE": "0",
            "DJANGO_CSRF_COOKIE_SECURE": "no",
            "DJANGO_DB_ENGINE": "postgresql",
            "DJANGO_DB_NAME": "gymkhana-ci",
            "DJANGO_DB_USER": "gymkhana-ci",
            "DJANGO_DB_PASSWORD": "ci-only-not-a-real-password",
            "DJANGO_DB_HOST": "db.example.test",
            "DJANGO_DB_SSLMODE": "verify-full",
            "PYTHONPATH": str(ROOT / "KDF"),
        })
        result = subprocess.run(
            [sys.executable, "-c", (
                "from django.conf import settings; "
                "assert settings.DEBUG is False; "
                "assert settings.SECURE_SSL_REDIRECT is False; "
                "assert settings.SESSION_COOKIE_SECURE is False; "
                "assert settings.CSRF_COOKIE_SECURE is False"
            )],
            cwd=ROOT / "KDF",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_sqlite_is_restricted_to_debug_development(self):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "KDF.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key-with-at-least-fifty-characters-and-varied-alphabet",
            "DJANGO_DEBUG": "false",
            "DJANGO_DB_ENGINE": "sqlite",
            "PYTHONPATH": str(ROOT / "KDF"),
        })
        result = subprocess.run(
            [sys.executable, "-c", "from django.conf import settings; print(settings.DATABASES)"],
            cwd=ROOT / "KDF",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "DJANGO_DB_ENGINE=postgresql (or postgres) is required",
            result.stderr,
        )

        env["DJANGO_DEBUG"] = "true"
        result = subprocess.run(
            [sys.executable, "-c", (
                "from django.conf import settings; "
                "assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'"
            )],
            cwd=ROOT / "KDF",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_postgresql_requires_certificate_verification_and_valid_bounds(self):
        base = {
            "DJANGO_SETTINGS_MODULE": "KDF.settings",
            "DJANGO_SECRET_KEY": "test-only-settings-key-with-at-least-fifty-characters-and-varied-alphabet",
            "DJANGO_DEBUG": "false",
            "DJANGO_ALLOWED_HOSTS": "app.example.test",
            "DJANGO_DB_ENGINE": "postgresql",
            "DJANGO_DB_NAME": "gymkhana",
            "DJANGO_DB_USER": "gymkhana_app",
            "DJANGO_DB_PASSWORD": "ci-only-not-a-real-password",
            "DJANGO_DB_HOST": "db.example.test",
            "PYTHONPATH": str(ROOT / "KDF"),
        }
        valid = os.environ.copy()
        valid.update({
            **base,
            "DJANGO_DB_SSLMODE": "verify-full",
            "DJANGO_DB_SSLROOTCERT": "/etc/ssl/certs/provider-ca.pem",
            "DJANGO_DB_PORT": "6432",
        })
        result = subprocess.run(
            [sys.executable, "-c", (
                "from django.conf import settings; "
                "db=settings.DATABASES['default']; "
                "assert db['ENGINE'] == 'django.db.backends.postgresql'; "
                "assert db['OPTIONS'] == {'sslmode': 'verify-full', "
                "'sslrootcert': '/etc/ssl/certs/provider-ca.pem'}; "
                "assert db['PORT'] == '6432'; "
                "assert db['CONN_HEALTH_CHECKS'] is True"
            )],
            cwd=ROOT / "KDF",
            env=valid,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

        # Direct TCP/PostgreSQL connections must default to full certificate
        # and hostname verification when no SSL mode is explicitly supplied.
        default_tls = os.environ.copy()
        default_tls.update(base)
        result = subprocess.run(
            [sys.executable, "-c", (
                "from django.conf import settings; "
                "assert settings.DATABASES['default']['OPTIONS']['sslmode'] == 'verify-full'"
            )],
            cwd=ROOT / "KDF",
            env=default_tls,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

        # Google Cloud SQL Auth Proxy owns the TLS tunnel for its local Unix
        # socket, so the client-side socket must use sslmode=disable.
        proxy_env = os.environ.copy()
        proxy_env.update({
            **base,
            "DJANGO_DB_HOST": "/cloudsql/project:region:instance",
        })
        result = subprocess.run(
            [sys.executable, "-c", (
                "from django.conf import settings; db=settings.DATABASES['default']; "
                "assert db['HOST'] == '/cloudsql/project:region:instance'; "
                "assert db['OPTIONS']['sslmode'] == 'disable'"
            )],
            cwd=ROOT / "KDF",
            env=proxy_env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

        invalid_overrides = (
            {"DJANGO_DB_SSLMODE": "disable"},
            {"DJANGO_DB_SSLMODE": "prefer"},
            {"DJANGO_DB_SSLMODE": "require"},
            {"DJANGO_DB_PORT": "not-a-port"},
            {"DJANGO_DB_PORT": "70000"},
            {"DJANGO_DB_CONN_MAX_AGE": "not-an-integer"},
            {"DJANGO_DB_CONN_MAX_AGE": "-1"},
            {"DJANGO_DB_CONN_MAX_AGE": "3601"},
        )
        for overrides in invalid_overrides:
            with self.subTest(overrides=overrides):
                env = os.environ.copy()
                env.update({**base, **overrides})
                result = subprocess.run(
                    [sys.executable, "-c", "from django.conf import settings; print(settings.DATABASES)"],
                    cwd=ROOT / "KDF",
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                if "DJANGO_DB_SSLMODE" in overrides:
                    self.assertIn("must verify the server certificate", result.stderr)

    def test_env_example_contains_only_secret_placeholders(self):
        example = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("DJANGO_SECRET_KEY=\n", example)
        self.assertNotIn("AIza", example)


if __name__ == "__main__":
    unittest.main(verbosity=2)
