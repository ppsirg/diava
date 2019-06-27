from django.db import models


class Cargo(models.Model):
    """docstring for Cargo."""
    nombre = models.CharField()
    descripcion = models.TextField()

    def __str__(self):
        return '{0.nombre}'.format(self)


class Usuario(models.Model):
    """docstring for Usuario."""
    nombre_completo = models.CharField()
    cargo = models.ForeignKey(Cargo)
    email = models.EmailField()
    telefono = models.CharField()

    def __str__(self):
        return '{0.cargo} - {0.nombre}'.format(self)
