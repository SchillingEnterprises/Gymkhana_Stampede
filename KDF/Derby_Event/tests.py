"""Django integration tests for the Gymkhana public pages and account routes."""
from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class PublicPageTests(TestCase):
    def test_public_pages_render_their_django_templates(self):
        expected = {
            "index": "index.html",
            "landing_page": "landing_page.html",
            "rules": "rules.html",
            "louisville_concierge": "louisville_concierge.html",
        }
        for route_name, template_name in expected.items():
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)

    def test_login_route_delegates_to_allauth(self):
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("account_login"), fetch_redirect_response=False)

    def test_signup_route_explains_registration_is_paused_without_opening_signup(self):
        self.assertFalse(settings.ACCOUNT_SIGNUP_ENABLED)
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration_paused.html")
        self.assertContains(response, "Registration is temporarily paused")
        self.assertContains(response, reverse("login"))
