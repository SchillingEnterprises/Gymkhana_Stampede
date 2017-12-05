from django.core.urlresolvers import reverse
from django.db import models as models
from django.db.models import *

# STATUS_CHOICES = (
#     ('i', 'In Progress'),
#     ('r', 'In Review'),
#     ('p', 'Published'),
# )


class ChurchGoer(models.Model):
    # Fields
    first_name = CharField(max_length=255)
    middle_name = CharField(max_length=255, blank=True)
    maiden_name = CharField(max_length=255)
    nickname = CharField(max_length=255, blank=True)
    birthday = DateTimeField(blank=True)
    name_of_guardian = CharField(max_length=750)
    home_church = CharField(max_length=500, blank=True)
    family_are_beargrass_members = BooleanField()
    address = TextField(blank=True)
    email = EmailField(blank=True)
    school = CharField(max_length=500, blank=True)
    degree = TextField(blank=True)
    employer = CharField(max_length=500, blank=True)
    gender = CharField(max_length=3)
    facebook_URL = URLField(blank=True)
    google_plus_URL = URLField(blank=True)
    instagram_URL = URLField(blank=True)
    snapchat_URL = URLField(blank=True)
    twitter_URL = URLField(blank=True)
    married = BooleanField(blank=True)
    name_of_spouse = CharField(max_length=750, blank=True)
    name_of_child = CharField(max_length=750, blank=True)
    surname = CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('youth_churchgoer_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('youth_churchgoer_update', args=(self.pk,))
