from django.shortcuts import redirect, render


def index(request):
    return render(request, "index.html")


def landing_page(request):
    return render(request, "landing_page.html")


def login(request):
    """Use django-allauth's real login flow instead of a non-functional mock form."""
    return redirect("account_login")


def louisville_concierge(request):
    return render(request, "louisville_concierge.html")


def register(request):
    """Explain that public signup is paused until safe participant onboarding is ready."""
    return render(request, "registration_paused.html")


def rules(request):
    return render(request, "rules.html")
