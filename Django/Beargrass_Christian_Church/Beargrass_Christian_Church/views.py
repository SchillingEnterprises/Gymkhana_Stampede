from django.views.generic.base import TemplateView

from youth.models import ChurchGoer


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['__all__'] = ChurchGoer.objects.all()[:5]
        return context


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games_today'] = 6
        return context
