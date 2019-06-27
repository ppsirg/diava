from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .models import RondaPruebas, RondaReporte


class RondaPruebasDetailView(DetailView):
    model = RondaPruebas
    slug_field = 'SLUG_FIELD'
    slug_url_kwarg = 'SLUG_URL_KWARG'
    success_url = 'SUCCESS_URL'
    template_name = 'TEMPLATE_NAME'

class RondaListView(ListView):
    model = RondaPruebas
