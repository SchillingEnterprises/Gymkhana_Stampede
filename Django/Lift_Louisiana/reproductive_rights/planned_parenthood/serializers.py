from . import models

from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = (
            'pk',
            'address',
            'city',
            'state',
            'zip_code',
        )


class LegislationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Legislation
        fields = (
            'pk',
            'name',
            'authors',
            'chamber',
            'strategic_plan',
            'effective',
            'favorable',
            'is_law',
            'was_defeated',
        )


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Staff
        fields = (
            'pk',
            'credentials',
            'specialty',
            'active',
        )


class ClinicSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Clinic
        fields = (
            'pk',
            'active',
        )


class RevenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Revenue
        fields = (
            'pk',
            'created',
            'last_updated',
            'transaction',
            'donation',
            'income',
            'investment',
            'expense',
        )


class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Volunteer
        fields = (
            'pk',
            'active',
            'internal_projects_worked_on',
        )


class DemographicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Demographics
        fields = (
            'pk',
            'title',
            'first_name',
            'middle_name',
            'last_name',
            'suffix',
            'email_address',
        )
