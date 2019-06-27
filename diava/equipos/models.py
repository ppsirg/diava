from django.db import models


class Documento(object):
    """docstring for Documento."""
    nombre = models.CharField()
    descripcion = models.TextField()
    archivo = models.FileField()

    def __str__(self):
        return '{0.nombre}'.format(self)


class Equipo(models.Model):
    """docstring for Equipo."""
    codigo = models.CharField()
    marca = models.CharField()
    documentos = models.ManyToManyField(Documento)

    def __str__(self):
        return '{0.codigo}'.format(self)
