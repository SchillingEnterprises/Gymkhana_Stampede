"""Source contracts for the restored Gymkhana Django template routes."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "KDF" / "Derby_Event"
TEMPLATES = APP / "templates"


class GymkhanaTemplateResolutionTests(unittest.TestCase):
    def test_every_rendered_template_exists_in_django_template_directory(self):
        views = (APP / "views.py").read_text(encoding="utf-8")
        for name in ("index.html", "landing_page.html", "louisville_concierge.html", "rules.html"):
            with self.subTest(template=name):
                self.assertIn(f'"{name}"', views)
                self.assertTrue((TEMPLATES / name).is_file())

    def test_pages_extend_shared_accessible_base(self):
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        self.assertIn('lang="en"', base)
        self.assertIn('href="#main-content"', base)
        self.assertIn('id="main-content"', base)
        self.assertIn("bootstrap@5.3.9/dist/css/bootstrap.min.css", base)
        self.assertIn("bootstrap@5.3.9/dist/js/bootstrap.bundle.min.js", base)
        self.assertIn("integrity=", base)
        self.assertIn("data-bs-toggle", base)
        for name in ("index.html", "landing_page.html", "louisville_concierge.html", "rules.html"):
            with self.subTest(template=name):
                self.assertIn('{% extends "base.html" %}', (TEMPLATES / name).read_text(encoding="utf-8"))

    def test_login_and_signup_use_real_allauth_routes_not_static_mock_forms(self):
        views = (APP / "views.py").read_text(encoding="utf-8")
        self.assertIn('return redirect("account_login")', views)
        self.assertIn('return redirect("account_signup")', views)

    def test_unimplemented_participation_features_are_not_advertised_as_live(self):
        rules = (TEMPLATES / "rules.html").read_text(encoding="utf-8")
        landing = (TEMPLATES / "landing_page.html").read_text(encoding="utf-8")
        self.assertIn("not currently active", rules)
        self.assertIn("not enabled", landing)
        self.assertIn("No submissions are being collected", landing)

    def test_original_static_archive_is_preserved(self):
        original = ROOT / "KDF/Derby_Event/static/Derby_Event/templates/html/index.html"
        self.assertTrue(original.is_file())
        self.assertTrue((APP / "static/Derby_Event/css/app.css").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
