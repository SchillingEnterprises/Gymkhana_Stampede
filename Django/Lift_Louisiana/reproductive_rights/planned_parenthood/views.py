from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Location, Legislation, Staff, Clinic, Revenue, Volunteer, Demographics
from .forms import LocationForm, LegislationForm, StaffForm, ClinicForm, RevenueForm, VolunteerForm, DemographicsForm


class LocationListView(ListView):
    model = Location


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm


class LocationDetailView(DetailView):
    model = Location


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm


class LegislationListView(ListView):
    model = Legislation


class LegislationCreateView(CreateView):
    model = Legislation
    form_class = LegislationForm


class LegislationDetailView(DetailView):
    model = Legislation


class LegislationUpdateView(UpdateView):
    model = Legislation
    form_class = LegislationForm


class StaffListView(ListView):
    model = Staff


class StaffCreateView(CreateView):
    model = Staff
    form_class = StaffForm


class StaffDetailView(DetailView):
    model = Staff


class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm


class ClinicListView(ListView):
    model = Clinic


class ClinicCreateView(CreateView):
    model = Clinic
    form_class = ClinicForm


class ClinicDetailView(DetailView):
    model = Clinic


class ClinicUpdateView(UpdateView):
    model = Clinic
    form_class = ClinicForm


class RevenueListView(ListView):
    model = Revenue


class RevenueCreateView(CreateView):
    model = Revenue
    form_class = RevenueForm


class RevenueDetailView(DetailView):
    model = Revenue


class RevenueUpdateView(UpdateView):
    model = Revenue
    form_class = RevenueForm


class VolunteerListView(ListView):
    model = Volunteer


class VolunteerCreateView(CreateView):
    model = Volunteer
    form_class = VolunteerForm


class VolunteerDetailView(DetailView):
    model = Volunteer


class VolunteerUpdateView(UpdateView):
    model = Volunteer
    form_class = VolunteerForm


class DemographicsListView(ListView):
    model = Demographics


class DemographicsCreateView(CreateView):
    model = Demographics
    form_class = DemographicsForm


class DemographicsDetailView(DetailView):
    model = Demographics


class DemographicsUpdateView(UpdateView):
    model = Demographics
    form_class = DemographicsForm
