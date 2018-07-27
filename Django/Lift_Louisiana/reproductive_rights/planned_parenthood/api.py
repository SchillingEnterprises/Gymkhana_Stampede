from . import models
from . import serializers
from rest_framework import viewsets, permissions


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Location class"""

    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class LegislationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Legislation class"""

    queryset = models.Legislation.objects.all()
    serializer_class = serializers.LegislationSerializer
    permission_classes = [permissions.IsAuthenticated]


class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet for the Staff class"""

    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClinicViewSet(viewsets.ModelViewSet):
    """ViewSet for the Clinic class"""

    queryset = models.Clinic.objects.all()
    serializer_class = serializers.ClinicSerializer
    permission_classes = [permissions.IsAuthenticated]


class RevenueViewSet(viewsets.ModelViewSet):
    """ViewSet for the Revenue class"""

    queryset = models.Revenue.objects.all()
    serializer_class = serializers.RevenueSerializer
    permission_classes = [permissions.IsAuthenticated]


class VolunteerViewSet(viewsets.ModelViewSet):
    """ViewSet for the Volunteer class"""

    queryset = models.Volunteer.objects.all()
    serializer_class = serializers.VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]


class DemographicsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Demographics class"""

    queryset = models.Demographics.objects.all()
    serializer_class = serializers.DemographicsSerializer
    permission_classes = [permissions.IsAuthenticated]
