from django import forms
from .models import Location, Legislation, Staff, Clinic, Revenue, Volunteer, Demographics


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['address', 'city', 'state', 'zip_code']


class LegislationForm(forms.ModelForm):
    class Meta:
        model = Legislation
        fields = ['name', 'authors', 'chamber', 'strategic_plan', 'effective', 'favorable', 'is_law', 'was_defeated',
                  'location']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['credentials', 'specialty', 'active', 'staff_member']


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['active', 'staff']


class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = ['transaction', 'donation', 'income', 'investment', 'expense', 'transactor']


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['active', 'internal_projects_worked_on', 'volunteer', 'location']


class DemographicsForm(forms.ModelForm):
    class Meta:
        model = Demographics
        fields = ['title', 'first_name', 'middle_name', 'last_name', 'suffix', 'email_address', 'location']
