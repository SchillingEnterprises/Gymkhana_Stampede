import unittest

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from .models import ChurchGoer


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


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


def create_churchgoer(**kwargs):
    defaults = {'first_name': "first_name", 'middle_name': "middle_name", 'maiden_name': "maiden_name",
                'nickname': "nickname", 'birthday': "birthday", 'name_of_guardian': "name_of_guardian",
                'home_church': "home_church", 'family_are_beargrass_members': "family_are_beargrass_members",
                'address': "address", 'email': "email", 'school': "school", 'degree': "degree",
                'employer': "employer", 'gender': "gender", 'facebook_URL': "facebook_URL",
                'google_plus_URL': "google_plus_URL", 'instagram_URL': "instagram_URL", 'snapchat_URL': "snapchat_URL",
                'twitter_URL': "twitter_URL", 'married': "married", 'name_of_spouse': "name_of_spouse",
                'name_of_child': "name_of_child", 'surname': "surname"}
    defaults.update(**kwargs)
    return ChurchGoer.objects.create(**defaults)


class ChurchGoerViewTest(unittest.TestCase):
    """Tests for ChurchGoer"""
    def setUp(self):
        self.client = Client()

    def test_list_churchgoer(self):
        url = reverse('youth_churchgoer_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_churchgoer(self):
        url = reverse('youth_churchgoer_create')
        data = {'first_name': "first_name", 'middle_name': "middle_name", 'maiden_name': "maiden_name",
                'nickname': "nickname", 'birthday': "birthday", 'name_of_guardian': "name_of_guardian",
                'home_church': "home_church", 'family_are_beargrass_members': "family_are_beargrass_members",
                'address': "address", 'email': "email", 'school': "school", 'degree': "degree",
                'employer': "employer", 'gender': "gender", 'facebook_URL': "facebook_URL",
                'google_plus_URL': "google_plus_URL", 'instagram_URL': "instagram_URL", 'snapchat_URL': "snapchat_URL",
                'twitter_URL': "twitter_URL", 'married': "married", 'name_of_spouse': "name_of_spouse",
                'name_of_child': "name_of_child", 'surname': "surname"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_churchgoer(self):
        churchgoer = create_churchgoer()
        url = reverse('youth_churchgoer_detail', args=[churchgoer.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_churchgoer(self):
        churchgoer = create_churchgoer()
        data = {'first_name': "first_name", 'middle_name': "middle_name", 'maiden_name': "maiden_name",
                'nickname': "nickname", 'birthday': "birthday", 'name_of_guardian': "name_of_guardian",
                'home_church': "home_church", 'family_are_beargrass_members': "family_are_beargrass_members",
                'address': "address", 'email': "email", 'school': "school", 'degree': "degree",
                'employer': "employer", 'gender': "gender", 'facebook_URL': "facebook_URL",
                'google_plus_URL': "google_plus_URL", 'instagram_URL': "instagram_URL", 'snapchat_URL': "snapchat_URL",
                'twitter_URL': "twitter_URL", 'married': "married", 'name_of_spouse': "name_of_spouse",
                'name_of_child': "name_of_child", 'surname': "surname"}
        url = reverse('youth_churchgoer_update', args=[churchgoer.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
