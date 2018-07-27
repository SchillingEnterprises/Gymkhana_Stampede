from django.views import generic

from .models import Transaction


class IndexView(generic.ListView):
    template_name = 'seimes2/index.html'
    context_object_name = 'latest_transaction_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Transaction.objects.order_by('-store_branch')[:5]


class DetailView(generic.DetailView):
    model = Transaction
    template_name = 'seimes2/detail.html'
