# -*- coding: utf-8 -*-
"""
Procesamiento de datos
"""
import os
import json
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
from hashlib import blake2b
from jinja2 import Template
from django.db import models
from equipos.models import Equipo
from .data_processing import ProcesamientoMedicion


class ConfiguracionSensor(models.Model):
    """docstring for Sensor."""
    limite_inferior = models.FloatField()
    limite_superior = models.FloatField()
    tolerancia = models.FloatField()

    def __str__(self):
        return '[{0.limite_inferior}-{0.limite_superior}] {0.tolerancia}'.format(self)


class Medicion(models.Model, ProcesamientoMedicion):
    """docstring for Medicion."""
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(blank=True, default=datetime.datetime.now)
    equipo = models.ForeignKey(Equipo)
    archivo = models.FileField(upload_to='/mediciones')
    registro_datos = models.TextField(blank=True, null=True)
    configuraciones = models.ManyToManyField(ConfiguracionSensor)
    ruta_grafica = models.CharField(blank=True, max_length=100)
    datos = None

    @property
    def grafico(self):
        return '{}.png'.format(medicion.nombre_grafico),

    @property
    def datos_tabla(self):
        # crear datos para reporte html
        if not self.datos:
            self.iniciar(self.nombre, self.equipo.codigo, self.configuraciones)
        #hallar minimos y maximos y porcentaje de puntos por fuera
        dist = self.calcular_fuera_rango()
        max_min = self.calcular_maximos_minimos()
        #hallar promedio y desviacion estandar
        prom_desv = self.calcular_promedio_desviacion()
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
