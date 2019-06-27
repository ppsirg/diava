from django.db import models
from equipos.models import Equipo


class ConfiguracionSensor(models.Model):
    """docstring for Sensor."""
    limite_inferior = models.FloatField()
    limite_superior = models.FloatField()
    tolerancia = models.FloatField()

    def __str__(self):
        return '[{0.limite_inferior}-{0.limite_superior}] {0.tolerancia}'.format(self)


class Medicion(models.Model):
    """docstring for Medicion."""
    nombre = models.CharField()
    fecha = models.DateField()
    equipo = models.ForeignKey(Equipo)
    archivo = models.FileField()
    configuraciones = models.ManyToManyField(ConfiguracionSensor)

    def __str__(self):
        return '{0.fecha.year}/{0.fecha.month} {0.equipo.codigo}'.format(self)
