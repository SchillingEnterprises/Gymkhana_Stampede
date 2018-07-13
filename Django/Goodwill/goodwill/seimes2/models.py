import datetime

from djmoney.models.fields import MoneyField
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField
from django.utils import timezone
from django.db import models


class Customer(models.Model):
    title = models.CharField(max_length=30)
    first_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=600)
    suffix = models.CharField(max_length=5)
    street_address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=58)
    state = USStateField(_("state"), default="KY")
    zip_code = models.CharField(_("zip code"), max_length=5)


class Employee(models.Model):
    title = models.CharField(max_length=30)
    first_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=600)
    suffix = models.CharField(max_length=5)
    street_address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=58)
    state = USStateField(_("state"), default="KY")
    zip_code = models.CharField(_("zip code"), max_length=5)


class Inventory(models.Model):
    iuid = models.TextField()
    category = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    checked_in = models.DateField(auto_created=True)
    sale_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    sold_date = models.DateField()


class StoreBranch(models.Model):
    name = models.CharField(max_length=500)
    id = models.IntegerField(primary_key=True)
    street_address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=58)
    state = USStateField(_("state"), default="KY")
    zip_code = models.CharField(_("zip code"), max_length=5)


class Transaction(models.Model):
    store_branch = models.ForeignKey(StoreBranch, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=5000)
    upt = models.Count
