"""Static contracts for the legacy Django project that do not install old dependencies."""
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
    def test_models_match_preserved_profile_schema_and_checkpoint_fields(self):
        nodes = class_nodes(parse(APP / "models.py"))
        self.assertTrue({"User", "Checkpoint", "Event", "Reward"}.issubset(nodes))
        self.assertTrue(
            {"first_name", "last_name", "email_address", "birthday", "location", "proof"}
            .issubset(assigned_names(nodes["User"]))
        )
        self.assertTrue(
            {"name", "location", "photograph", "information", "isValid"}
            .issubset(assigned_names(nodes["Checkpoint"]))
        )

    def test_model_string_representations_return_text(self):
        nodes = class_nodes(parse(APP / "models.py"))
        for name in ("User", "Checkpoint", "Event", "Reward"):
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
                self.assertIsInstance(returns[0].value, (ast.Attribute, ast.Call))

    def test_checkpoint_schema_extension_has_non_destructive_defaults(self):
        migration = (APP / "migrations" / "0002_checkpoint_fields.py").read_text(encoding="utf-8")
        self.assertIn('dependencies = [', migration)
        self.assertIn('("Derby_Event", "0001_initial")', migration)
        self.assertIn('name="name"', migration)
        self.assertIn('name="isValid"', migration)
        self.assertIn('default=""', migration)
        self.assertIn('default=False', migration)

    def test_admin_imports_only_models_that_exist(self):
        tree = parse(APP / "admin.py")
        imports = {
            alias.name
            for node in tree.body if isinstance(node, ast.ImportFrom)
            for alias in node.names
            if node.module == "models"
        }
        self.assertTrue({"User", "Event", "Checkpoint", "Reward"}.issubset(imports))

    def test_url_configuration_uses_supported_django_url_imports(self):
        project = (PROJECT / "urls.py").read_text(encoding="utf-8")
        app = (APP / "urls.py").read_text(encoding="utf-8")
        self.assertIn("from django.urls import include, path", project)
        self.assertNotIn("django.contrib.auth.urls import url", project)
        self.assertIn("from django.urls import path", app)
        self.assertNotIn("django.conf.urls import url", app)


if __name__ == "__main__":
    unittest.main(verbosity=2)
