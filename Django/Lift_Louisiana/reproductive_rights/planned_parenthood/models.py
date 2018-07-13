from django.db import models as models
from django.db.models import *
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from .utils import ChoiceEnum


# Create your models here.
class State(ChoiceEnum):
    ALABAMA = 'AL'
    ALASKA = 'AK'
    ARIZONA = 'AZ'
    ARKANSAS = 'AR'
    CALIFORNIA = 'CA'
    COLORADO = 'CO'
    CONNECTICUT = 'CT'
    DELAWARE = 'DE'
    FLORIDA = 'FL'
    GEORGIA = 'GA'
    HAWAII = 'HI'
    IDAHO = 'ID'
    ILLINOIS = 'IL'
    INDIANA = 'IN'
    IOWA = 'IA'
    KANSAS = 'KS'
    KENTUCKY = 'KY'
    LOUISIANA = 'LA'
    MAINE = 'ME'
    MARYLAND = 'MD'
    MASSACHUSETTS = 'MA'
    MICHIGAN = 'MI'
    MINNESOTA = 'MN'
    MISSISSIPPI = 'MS'
    MISSOURI = 'MO'
    MONTANA = 'MT'
    NEBRASKA = 'NE'
    NEVADA = 'NV'
    NEW_HAMPSHIRE = 'NH'
    NEW_JERSEY = 'NJ'
    NEW_MEXICO = 'NM'
    NEW_YORK = 'NY'
    NORTH_CAROLINA = 'NC'
    NORTH_DAKOTA = 'ND'
    OHIO = 'OH'
    OKLAHOMA = 'OK'
    OREGON = 'OR'
    PENNSYLVANIA = 'PA'
    RHODE_ISLAND = 'RI'
    SOUTH_CAROLINA = 'SC'
    SOUTH_DAKOTA = 'SD'
    TENNESSEE = 'TN'
    TEXAS = 'TX'
    UTAH = 'UT'
    VERMONT = 'VT'
    VIRGINIA = 'VA'
    WASHINGTON = 'WA'
    WEST_VIRGINIA = 'WV'
    WISCONSIN = 'WI'
    WYOMING = 'WY'
    AMERICAN_SAMOA = 'AS'
    DISTRICT_OF_COLUMBIA = 'DC'
    FEDERATED_STATES_OF_MICRONESIA = 'FM'
    GUAM = 'GU'
    MARSHALL_ISLANDS = 'MH'
    NORTHERN_MARIANA_ISLANDS = 'MP'
    PALAU = 'PW'
    PUERTO_RICO = 'PR'
    VIRGIN_ISLANDS = 'VI'
    ARMED_FORCES_AMERICAS = 'AA'
    ARMED_FORCES_AFRICA_CANADA_EUROPE_MIDDLE_EAST = 'AE'
    ARMED_FORCES_PACIFIC = 'AP'


class Title(ChoiceEnum):
    DOCTOR = 'Dr.'
    ESQUIRE = 'Esq.'
    HONORABLE = 'Hon.'
    JUNIOR = 'Jr.'
    LADY = 'Lady'
    LORD = 'Lord'
    MISS = 'Miss'
    MESDAMES = 'Mmes'
    MISTER = 'Mr.'
    MISSES = 'Mrs.'
    MIZ = 'Ms.'
    MONSIGNOR = 'Msgr.'
    PROFESSOR = 'Prof.'
    REVEREND = 'Rev.'
    RIGHT_HONORABLE = 'Rt. Hon.'
    SIR = 'Sir'
    SENIOR = 'Sr.'
    SAINT = 'St.'


class Suffix(ChoiceEnum):
    SENIOR = 'Sr.'
    JUNIOR = 'Jr.'
    SECOND = 'II'
    THIRD = 'III'
    FOURTH = 'IV'


class Location(models.Model):
    # Fields
    address = TextField()
    city = CharField(max_length=250, null=True)
    state = CharField(max_length=2, choices=State.choices(), null=True)
    zip_code = PositiveIntegerField()

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('location_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('location_update', args=(self.pk,))


class Demographics(models.Model):
    # Fields
    title = models.CharField(max_length=7, choices=Title.choices(), null=True)
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=500, null=True)
    suffix = models.CharField(max_length=3, choices=Suffix.choices(), null=True)
    email_address = models.EmailField()

    # Relationship Fields
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('demographics_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('demographics_update', args=(self.pk,))


class Legislation(models.Model):
    # Fields
    name = CharField(max_length=1000, null=True)
    authors = TextField()
    chamber = TextField()
    strategic_plan = TextField()
    effective = DateField()
    favorable = BooleanField()
    is_law = BooleanField()
    was_defeated = BooleanField()

    # Relationship Fields
    location = ForeignKey(
        Location, on_delete=models.CASCADE, null=True
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('legislation_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('legislation_update', args=(self.pk,))


class Staff(models.Model):
    # Fields
    credentials = TextField()
    specialty = TextField()
    active = BooleanField()

    # Relationship Fields
    staff_member = models.ForeignKey(Demographics, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('staff_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('staff_update', args=(self.pk,))


class Clinic(models.Model):
    # Fields
    active = BooleanField()

    # Relationship Fields
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('clinic_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('clinic_update', args=(self.pk,))


class Revenue(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    transaction = models.FloatField()
    donation = models.BooleanField()
    income = models.BooleanField()
    investment = models.BooleanField()
    expense = models.BooleanField()

    # Relationship Fields
    transactor = models.ForeignKey(Staff, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('revenue_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('revenue_update', args=(self.pk,))


class Volunteer(models.Model):
    # Fields
    active = models.BooleanField()
    internal_projects_worked_on = models.TextField()

    # Relationship Fields
    volunteer = models.ForeignKey(Demographics, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('volunteer_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('volunteer_update', args=(self.pk,))
