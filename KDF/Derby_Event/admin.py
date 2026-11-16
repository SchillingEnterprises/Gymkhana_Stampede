"""Django admin registrations for the event-domain models."""
from django.contrib import admin

from .models import Checkpoint, Event, Reward, User


admin.site.register((User, Event, Checkpoint, Reward))
