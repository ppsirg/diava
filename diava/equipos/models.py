# -*- coding: utf-8 -*-
from django.db import models


class Documento(models.Model):
    """Documento asociado a un equipo"""
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='documents/')

    def __str__(self):
        return '{0.nombre}'.format(self)


class Equipo(models.Model):
    """docstring for Equipo."""
    codigo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50, null=True)
    documentos = models.ManyToManyField(Documento)
    fecha_creacion = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __str__(self):
        return '{0.codigo}'.format(self)
