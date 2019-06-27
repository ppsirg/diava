from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .forms import EquipoForm


class EquipoCreateView(CreateView):
    model = Equipo
    form_class = FORM_CLASS
    success_url = 'SUCCESS_URL'
    template_name = 'TEMPLATE_NAME'


class EquipoUpdateView(UpdateView):
    model = Equipo
    template_name = 'TEMPLATE_NAME'


class EquipoDeleteView(DeleteView):
    model = Equipo
    template_name = 'TEMPLATE_NAME'


class EquipoDetailView(DetailView):
    model = Equipo
    slug_field = 'SLUG_FIELD'
    slug_url_kwarg = 'SLUG_URL_KWARG'
    success_url = 'SUCCESS_URL'
    template_name = 'TEMPLATE_NAME'
