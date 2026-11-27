"""Static contracts for the legacy Django project without installing its old stack."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "KDF" / "Derby_Event"
PROJECT = ROOT / "KDF" / "KDF"


def parse(path):
    return ast.parse(path.read_text(encoding="utf-8"))


def class_nodes(tree):
    return {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}


def assigned_names(node):
    names = set()
    for item in node.body:
        if isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            names.add(item.target.id)
    return names


class DjangoApplicationContractTests(unittest.TestCase):
    def test_models_express_participant_checkpoint_event_and_reward_domains(self):
        nodes = class_nodes(parse(APP / "models.py"))
        self.assertTrue({"Participant", "Checkpoint", "Event", "Reward"}.issubset(nodes))
        self.assertNotIn("User", nodes, "Participant profile must not impersonate Django authentication")
        self.assertTrue(
            {"account", "first_name", "last_name", "email_address", "birthday", "location", "proof"}
            .issubset(assigned_names(nodes["Participant"]))
        )
        self.assertTrue(
            {"name", "location", "photograph", "information", "is_valid"}
            .issubset(assigned_names(nodes["Checkpoint"]))
        )

    def test_domain_models_have_text_string_representations(self):
        nodes = class_nodes(parse(APP / "models.py"))
        for name in ("Participant", "Checkpoint", "Event", "Reward"):
            with self.subTest(model=name):
                methods = {
                    child.name: child
                    for child in nodes[name].body
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                }
                self.assertIn("__str__", methods)
                returns = [
                    item for item in ast.walk(methods["__str__"])
                    if isinstance(item, ast.Return)
                ]
                self.assertEqual(len(returns), 1)
                self.assertIsInstance(returns[0].value, (ast.Attribute, ast.Call, ast.JoinedStr))

    def test_checkpoint_fields_are_added_non_destructively(self):
        migration = (APP / "migrations" / "0002_checkpoint_fields.py").read_text(encoding="utf-8")
        self.assertIn('("Derby_Event", "0001_initial")', migration)
        self.assertIn('name="name"', migration)
        self.assertIn('name="isValid"', migration)
        self.assertIn('default=""', migration)
        self.assertIn('default=False', migration)

    def test_participant_migration_renames_the_existing_profile_table(self):
        migration = (APP / "migrations" / "0003_participant_domain.py").read_text(encoding="utf-8")
        self.assertIn('("Derby_Event", "0002_checkpoint_fields")', migration)
        self.assertIn('migrations.RenameModel(', migration)
        self.assertIn('old_name="User"', migration)
        self.assertIn('new_name="Participant"', migration)
        self.assertNotIn("migrations.CreateModel(", migration)
        self.assertIn('name="account"', migration)
        self.assertIn("null=True", migration)
        self.assertIn("OneToOneField", migration)

    def test_participant_migration_preserves_checkpoint_status_and_coordinate_strings(self):
        migration = (APP / "migrations" / "0003_participant_domain.py").read_text(encoding="utf-8")
        self.assertIn('old_name="isValid"', migration)
        self.assertIn('new_name="is_valid"', migration)
        self.assertIn('field=models.BooleanField(default=False)', migration)
        self.assertIn('field=models.CharField(blank=True, default="", max_length=42)', migration)
        self.assertNotIn("PositiveIntegerField", migration)

    def test_admin_registers_the_models_that_exist(self):
        tree = parse(APP / "admin.py")
        imported = {
            alias.name
            for node in tree.body if isinstance(node, ast.ImportFrom)
            for alias in node.names
            if node.module == "models"
        }
        self.assertTrue({"Participant", "Event", "Checkpoint", "Reward"}.issubset(imported))
        self.assertNotIn("User", imported)

    def test_url_configuration_uses_supported_django_url_imports(self):
        project = (PROJECT / "urls.py").read_text(encoding="utf-8")
        app = (APP / "urls.py").read_text(encoding="utf-8")
        self.assertIn("from django.urls import include, path", project)
        self.assertNotIn("django.contrib.auth.urls import url", project)
        self.assertIn("from django.urls import path", app)
        self.assertNotIn("django.conf.urls import url", app)


class RuntimeSecuritySettingsTests(unittest.TestCase):
    def setUp(self):
        self.settings = (PROJECT / "settings.py").read_text(encoding="utf-8")

    def test_secret_key_is_required_and_never_has_a_committed_fallback(self):
        self.assertIn('SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")', self.settings)
        self.assertIn('if not SECRET_KEY or not SECRET_KEY.strip():', self.settings)
        self.assertIn('len(SECRET_KEY) < 50', self.settings)
        self.assertIn('len(set(SECRET_KEY)) < 5', self.settings)
        self.assertIn('raise ImproperlyConfigured("Set DJANGO_SECRET_KEY', self.settings)

    def test_debug_is_off_by_default_and_hosts_are_explicit(self):
        self.assertIn('DEBUG = env_bool("DJANGO_DEBUG", False)', self.settings)
        self.assertIn('os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")', self.settings)
        self.assertNotIn('"*"', self.settings)

    def test_csrf_authentication_and_browser_security_middleware_are_enabled(self):
        for middleware in (
            '"django.middleware.csrf.CsrfViewMiddleware"',
            '"django.contrib.auth.middleware.AuthenticationMiddleware"',
            '"django.middleware.clickjacking.XFrameOptionsMiddleware"',
        ):
            with self.subTest(middleware=middleware):
                self.assertIn(middleware, self.settings)
        self.assertIn("SECURE_CONTENT_TYPE_NOSNIFF = True", self.settings)
        self.assertIn('X_FRAME_OPTIONS = "DENY"', self.settings)
        self.assertIn('SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"', self.settings)

    def test_production_https_and_session_cookie_defaults_follow_debug_mode(self):
        self.assertIn('SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)', self.settings)
        self.assertIn('SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)', self.settings)
        self.assertIn('CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)', self.settings)
        self.assertIn("SESSION_COOKIE_HTTPONLY = True", self.settings)
        self.assertIn('SESSION_COOKIE_SAMESITE = "Lax"', self.settings)
        self.assertIn('CSRF_COOKIE_SAMESITE = "Lax"', self.settings)

    def test_postgresql_requires_environment_credentials_and_sqlite_remains_local_default(self):
        self.assertIn('DB_ENGINE = os.environ.get("DJANGO_DB_ENGINE", "sqlite")', self.settings)
        for variable in ("DJANGO_DB_NAME", "DJANGO_DB_USER", "DJANGO_DB_PASSWORD", "DJANGO_DB_HOST"):
            with self.subTest(variable=variable):
                self.assertIn('"'+variable+'"', self.settings)
        self.assertIn("if missing_db_values:", self.settings)
        self.assertIn('raise ImproperlyConfigured(', self.settings)
        self.assertIn('elif DB_ENGINE == "sqlite":', self.settings)


if __name__ == "__main__":
    unittest.main(verbosity=2)
