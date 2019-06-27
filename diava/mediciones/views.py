from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


class MedicionCreateView(CreateView):
    model = Medicion
    form_class = FORM_CLASS
    success_url = 'SUCCESS_URL'
    template_name = 'TEMPLATE_NAME'


class MedicionUpdateView(UpdateView):
    model = Medicion
    template_name = 'TEMPLATE_NAME'


class MedicionDeleteView(DeleteView):
    model = Equipo
    template_name = 'TEMPLATE_NAME'


class MedicionDetailView(DetailView):
    model = Medicion
    slug_field = 'SLUG_FIELD'
    slug_url_kwarg = 'SLUG_URL_KWARG'
    success_url = 'SUCCESS_URL'
    template_name = 'TEMPLATE_NAME'
