"""Project URL configuration for KDF."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("Derby_Event/", include("Derby_Event.urls")),
    path("admin/", admin.site.urls),
]
