"""Routes for the Derby Event application."""
from django.urls import path

from .views import index, landing_page, login, louisville_concierge, register, rules

urlpatterns = [
    path("rules/", rules, name="rules"),
    path("register/", register, name="register"),
    path("louisville_concierge/", louisville_concierge, name="louisville_concierge"),
    path("login/", login, name="login"),
    path("landing_page/", landing_page, name="landing_page"),
    path("", index, name="index"),
]
