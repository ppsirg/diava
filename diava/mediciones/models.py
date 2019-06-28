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
    datos = models.TextField(blank=True)
    configuraciones = models.ManyToManyField(ConfiguracionSensor)

    def grafico(self):
        return '{}.png'.format(medicion.nombre_grafico),

    def datos_tabla(self):
        # crear datos para reporte html
        reporte = []
        # crear reporte de promedio y desviacion para cada sensor (primeras tablas)
        for i in range(len(prom_desv['promedio']['sensores'])):
            reporte.append({
                'sensor': i+1,
                'promedio': prom_desv['promedio']['sensores'][i],
                'desviacion': prom_desv['desviacion']['sensores'][i]
                })
        # añadir el promedio y desviacion total al reporte creado
        reporte.append({
            'sensor': 'total',
            'promedio': prom_desv['promedio']['total'],
            'desviacion': prom_desv['desviacion']['total']
            })
        # guardar los reportes creados con la informacion de la medicion
        return reporte


    def __str__(self):
        return '{0.fecha.year}/{0.fecha.month} {0.equipo.codigo}'.format(self)
