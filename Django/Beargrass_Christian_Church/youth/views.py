from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rest_framework import generics

from youth.serializers import ChurchGoerSerializer
from youth.forms import ChurchGoerForm
from youth.models import ChurchGoer


def churchgoer_list(request):
    churchgoer = ChurchGoer.objects.all()
    return render(request, 'youth/churchgoer_list.html', {'Church Goer': churchgoer})


def churchgoer_detail(request, pk):
    churchgoer = get_object_or_404(ChurchGoer, pk=pk)
    return render(request, 'youth/churchgoer_detail.html', {'Church Goer': churchgoer})


class ChurchGoerListView(CreateView, ListView):
    context_object_name = 'youth'
    model = ChurchGoer
    template_name = 'youth/churchgoer_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChurchGoerListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ChurchGoerCreateView(LoginRequiredMixin, CreateView):
    model = ChurchGoer
    form_class = ChurchGoerForm
    page_title = 'Create Attendee'


class ChurchGoerDetailView(UpdateView, DetailView):
    model = ChurchGoer
    template_name = 'youth/churchgoer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ChurchGoerDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ChurchGoerUpdateView(LoginRequiredMixin, UpdateView):
    model = ChurchGoer
    form_class = ChurchGoerForm
    template_name_suffix = '_update_form'


class ChurchGoerDeleteView(LoginRequiredMixin, DeleteView):
    model = ChurchGoer
    success_url = reverse_lazy('churchgoer_list')


class ListCreateChurchGoer(generics.ListCreateAPIView):
    """Creates Church Goer List API"""
    queryset = ChurchGoer.objects.all()
    serializer_class = ChurchGoerSerializer

    def get_queryset(self):
        return self.queryset.filter(youth_id=self.kwargs.get('youth_pk'))

    def perform_create(self, serializer):
        churchgoer = get_object_or_404(
            ChurchGoer, pk=self.kwargs.get('churchgoer_pk')
        )
        serializer.save(churchgoer=churchgoer)


class RetrieveUpdateDestroyChurchGoer(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, Updates, & Deletes Church Goer via API"""
    queryset = ChurchGoer.objects.all()
    serializer_class = ChurchGoerSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            churchgoer_id=self.kwargs.get('churchgoer_pk'),
            pk=self.kwargs.get('pk')
        )


def search(request):
    term = request.GET.get('q')
    youth = ChurchGoer.objects.filter(
        Q(title__icontains=term) | Q(description__icontains=term),
        published=True
    )
    return render(request, 'youth/churchgoer_list.html', {'Youth': youth})
