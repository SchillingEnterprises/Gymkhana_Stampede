import unittest
from django.urls import reverse
from django.test import Client
from .models import Location, Legislation, Staff, Clinic, Revenue, Volunteer, Demographics
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {"username": "username", "email": "username@tempurl.com"}
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {"name": "group"}
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_location(**kwargs):
    defaults = {"address": "address", "city": "city", "state": "state", "zip_code": "zip_code"}
    defaults.update(**kwargs)
    return Location.objects.create(**defaults)


def create_legislation(**kwargs):
    defaults = {"name": "name", "authors": "authors", "chamber": "chamber", "strategic_plan": "strategic_plan",
                "effective": "effective", "favorable": "favorable", "is_law": "is_law", "was_defeated": "was_defeated"}
    defaults.update(**kwargs)
    if "location" not in defaults:
        defaults["location"] = create_location()
    return Legislation.objects.create(**defaults)


def create_staff(**kwargs):
    defaults = {"credentials": "credentials", "specialty": "specialty", "active": "active"}
    defaults.update(**kwargs)
    if "staff_member" not in defaults:
        defaults["staff_member"] = create_demographics()
    return Staff.objects.create(**defaults)


def create_clinic(**kwargs):
    defaults = {"active": "active"}
    defaults.update(**kwargs)
    if "staff" not in defaults:
        defaults["staff"] = create_staff()
    return Clinic.objects.create(**defaults)


def create_revenue(**kwargs):
    defaults = {"transaction": "transaction", "donation": "donation", "income": "income", "investment": "investment",
                "expense": "expense"}
    defaults.update(**kwargs)
    if "transactor" not in defaults:
        defaults["transactor"] = create_staff()
    return Revenue.objects.create(**defaults)


def create_volunteer(**kwargs):
    defaults = {"active": "active", "internal_projects_worked_on": "internal_projects_worked_on"}
    defaults.update(**kwargs)
    if "volunteer" not in defaults:
        defaults["volunteer"] = create_demographics()
    if "location" not in defaults:
        defaults["location"] = create_location()
    return Volunteer.objects.create(**defaults)


def create_demographics(**kwargs):
    defaults = {"title": "title", "first_name": "first_name", "middle_name": "middle_name", "last_name": "last_name",
                "suffix": "suffix", "email_address": "email_address"}
    defaults.update(**kwargs)
    if "location" not in defaults:
        defaults["location"] = create_location()
    return Demographics.objects.create(**defaults)


class LocationViewTest(unittest.TestCase):
    """
    Tests for Location
    """

    def setUp(self):
        self.client = Client()

    def test_list_location(self):
        url = reverse('location_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_location(self):
        url = reverse('location_create')
        data = {
            "address": "address",
            "city": "city",
            "state": "state",
            "zip_code": "zip_code",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_location(self):
        location = create_location()
        url = reverse('location_detail', args=[location.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_location(self):
        location = create_location()
        data = {
            "address": "address",
            "city": "city",
            "state": "state",
            "zip_code": "zip_code",
        }
        url = reverse('location_update', args=[location.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LegislationViewTest(unittest.TestCase):
    """
    Tests for Legislation
    """

    def setUp(self):
        self.client = Client()

    def test_list_legislation(self):
        url = reverse('legislation_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_legislation(self):
        url = reverse('legislation_create')
        data = {
            "name": "name",
            "authors": "authors",
            "chamber": "chamber",
            "strategic_plan": "strategic_plan",
            "effective": "effective",
            "favorable": "favorable",
            "is_law": "is_law",
            "was_defeated": "was_defeated",
            "location": create_location().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_legislation(self):
        legislation = create_legislation()
        url = reverse('legislation_detail', args=[legislation.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_legislation(self):
        legislation = create_legislation()
        data = {
            "name": "name",
            "authors": "authors",
            "chamber": "chamber",
            "strategic_plan": "strategic_plan",
            "effective": "effective",
            "favorable": "favorable",
            "is_law": "is_law",
            "was_defeated": "was_defeated",
            "location": create_location().pk,
        }
        url = reverse('legislation_update', args=[legislation.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class StaffViewTest(unittest.TestCase):
    """
    Tests for Staff
    """

    def setUp(self):
        self.client = Client()

    def test_list_staff(self):
        url = reverse('staff_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_staff(self):
        url = reverse('staff_create')
        data = {
            "credentials": "credentials",
            "specialty": "specialty",
            "active": "active",
            "staff_member": create_demographics().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_staff(self):
        staff = create_staff()
        url = reverse('staff_detail', args=[staff.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_staff(self):
        staff = create_staff()
        data = {
            "credentials": "credentials",
            "specialty": "specialty",
            "active": "active",
            "staff_member": create_demographics().pk,
        }
        url = reverse('staff_update', args=[staff.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ClinicViewTest(unittest.TestCase):
    """
    Tests for Clinic
    """

    def setUp(self):
        self.client = Client()

    def test_list_clinic(self):
        url = reverse('clinic_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_clinic(self):
        url = reverse('clinic_create')
        data = {
            "active": "active",
            "staff": create_staff().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_clinic(self):
        clinic = create_clinic()
        url = reverse('clinic_detail', args=[clinic.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_clinic(self):
        clinic = create_clinic()
        data = {
            "active": "active",
            "staff": create_staff().pk,
        }
        url = reverse('clinic_update', args=[clinic.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class RevenueViewTest(unittest.TestCase):
    """
    Tests for Revenue
    """

    def setUp(self):
        self.client = Client()

    def test_list_revenue(self):
        url = reverse('revenue_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_revenue(self):
        url = reverse('revenue_create')
        data = {
            "transaction": "transaction",
            "donation": "donation",
            "income": "income",
            "investment": "investment",
            "expense": "expense",
            "transactor": create_staff().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_revenue(self):
        revenue = create_revenue()
        url = reverse('revenue_detail', args=[revenue.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_revenue(self):
        revenue = create_revenue()
        data = {
            "transaction": "transaction",
            "donation": "donation",
            "income": "income",
            "investment": "investment",
            "expense": "expense",
            "transactor": create_staff().pk,
        }
        url = reverse('revenue_update', args=[revenue.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class VolunteerViewTest(unittest.TestCase):
    """
    Tests for Volunteer
    """

    def setUp(self):
        self.client = Client()

    def test_list_volunteer(self):
        url = reverse('volunteer_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_volunteer(self):
        url = reverse('volunteer_create')
        data = {
            "active": "active",
            "internal_projects_worked_on": "internal_projects_worked_on",
            "volunteer": create_demographics().pk,
            "location": create_location().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_volunteer(self):
        volunteer = create_volunteer()
        url = reverse('volunteer_detail', args=[volunteer.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_volunteer(self):
        volunteer = create_volunteer()
        data = {
            "active": "active",
            "internal_projects_worked_on": "internal_projects_worked_on",
            "volunteer": create_demographics().pk,
            "location": create_location().pk,
        }
        url = reverse('volunteer_update', args=[volunteer.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class DemographicsViewTest(unittest.TestCase):
    """
    Tests for Demographics
    """

    def setUp(self):
        self.client = Client()

    def test_list_demographics(self):
        url = reverse('demographics_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_demographics(self):
        url = reverse('demographics_create')
        data = {
            "title": "title",
            "first_name": "first_name",
            "middle_name": "middle_name",
            "last_name": "last_name",
            "suffix": "suffix",
            "email_address": "email_address",
            "location": create_location().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_demographics(self):
        demographics = create_demographics()
        url = reverse('demographics_detail', args=[demographics.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_demographics(self):
        demographics = create_demographics()
        data = {
            "title": "title",
            "first_name": "first_name",
            "middle_name": "middle_name",
            "last_name": "last_name",
            "suffix": "suffix",
            "email_address": "email_address",
            "location": create_location().pk,
        }
        url = reverse('demographics_update', args=[demographics.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
