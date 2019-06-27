from django.db import models
from usuarios.models import *
from equipos.models import *
from django.conf import settings

from datetime import timedelta

class RondaReporte(models.Model):
    equipo = models.ForeignKey(Equipo)
    estado = models.CharField(blank=True, max_length=100)
    date = models.DateField(default=datetime.datetime.today)
    historial = models.TextField(blank=True)

    class Meta:
        verbose_name = 'RondaReporte'
        verbose_name_plural = 'RondaReportes'

    def __str__(self):
        return '{}'.format(self)



class RondaPruebas(models.Model):
    fecha_inicio = models.DateField(default=datetime.datetime.today)
    fecha_fin = models.DateField(default=self.default_ending_date)
    responsable = models.ForeignKey(Usuario)
    equipos = models.ManyToManyField(RELATED_MODEL)
    reportes = models.ForeignKey(RondaReporte)
    porcentaje_completado = forms.FloatField()

    def default_ending_date(self):
        return datetime.datetime.today+timedelta(days=settings.DURACION_VIGENCIA_VALIDACION)


    def fecha_inicio_min(self):
        return self.fecha_inicio.strftime('%b/%Y')
    
    def fecha_fin_min(self):
        return self.fecha_fin.strftime('%b/%Y')

    class Meta:
        verbose_name = 'RondaPruebas'
        verbose_name_plural = 'RondaPruebass'

    def __str__(self):
        return '{}'.format(self)
