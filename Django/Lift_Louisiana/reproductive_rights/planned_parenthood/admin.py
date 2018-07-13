from django.contrib import admin
from django import forms
from .models import Location, Legislation, Staff, Clinic, Revenue, Volunteer, Demographics


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class LocationAdmin(admin.ModelAdmin):
    form = LocationAdminForm
    list_display = ['address', 'city', 'state', 'zip_code']
    readonly_fields = []


admin.site.register(Location, LocationAdmin)


class LegislationAdminForm(forms.ModelForm):
    class Meta:
        model = Legislation
        fields = '__all__'


class LegislationAdmin(admin.ModelAdmin):
    form = LegislationAdminForm
    list_display = ['name', 'authors', 'chamber', 'strategic_plan', 'effective', 'favorable', 'is_law', 'was_defeated']
    readonly_fields = []


admin.site.register(Legislation, LegislationAdmin)


class StaffAdminForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ['credentials', 'specialty', 'active']
    readonly_fields = []


admin.site.register(Staff, StaffAdmin)


class ClinicAdminForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = '__all__'


class ClinicAdmin(admin.ModelAdmin):
    form = ClinicAdminForm
    list_display = ['active']
    readonly_fields = []


admin.site.register(Clinic, ClinicAdmin)


class RevenueAdminForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = '__all__'


class RevenueAdmin(admin.ModelAdmin):
    form = RevenueAdminForm
    list_display = ['created', 'last_updated', 'transaction', 'donation', 'income', 'investment', 'expense']
    readonly_fields = []


admin.site.register(Revenue, RevenueAdmin)


class VolunteerAdminForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = '__all__'


class VolunteerAdmin(admin.ModelAdmin):
    form = VolunteerAdminForm
    list_display = ['active', 'internal_projects_worked_on']
    readonly_fields = []


admin.site.register(Volunteer, VolunteerAdmin)


class DemographicsAdminForm(forms.ModelForm):
    class Meta:
        model = Demographics
        fields = '__all__'


class DemographicsAdmin(admin.ModelAdmin):
    form = DemographicsAdminForm
    list_display = ['title', 'first_name', 'middle_name', 'last_name', 'suffix', 'email_address']
    readonly_fields = []


admin.site.register(Demographics, DemographicsAdmin)
