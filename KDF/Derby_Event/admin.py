"""Focused Django admin configuration for event-domain records."""
from django.contrib import admin

from .models import Checkpoint, Event, Participant, Reward


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email_address", "birthday")
    list_filter = ("birthday",)
    search_fields = ("first_name", "last_name", "email_address")
    ordering = ("last_name", "first_name")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "time", "point_value")
    list_filter = ("time",)
    search_fields = ("name", "location")
    ordering = ("time",)


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = ("name", "is_valid")
    list_filter = ("is_valid",)
    search_fields = ("name", "information")


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ("point_total",)
    ordering = ("-point_total",)
